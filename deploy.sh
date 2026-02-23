#!/bin/bash

SERVICE=""
VER=""
ENVIRON=""
REPO_LINK="https://github.com/varvarvara/sigma_backend"
DEPLOY_DIR=""
BACKUP_DIR=""
BACKUP_FILE=""

log_info() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log_error() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1" >&2
}

parse_args() {
    for arg in "$@"; do
        case $arg in
            --service=*) SERVICE="${arg#*=}" ;;
            --version=*) VER="${arg#*=}" ;;
            --env=*) ENVIRON="${arg#*=}" ;;
        esac
    done

    if [ -z "$SERVICE" ] || [ -z "$VER" ] || [ -z "$ENVIRON" ]; then
        log_error "Required arguments missing"
        echo "Usage: $0 --service=name --version=x.y.z --env=env"
        exit 1
    fi

    DEPLOY_DIR="/tmp/deploy_${SERVICE}"
    BACKUP_DIR="/tmp/backup_${SERVICE}"
}

check_dependencies() {
    log_info "Checking required tools..."
    for tool in git docker curl python3; do
        command -v $tool >/dev/null 2>&1 || { log_error "$tool not found"; exit 1; }
    done
    docker info >/dev/null 2>&1 || { log_error "Docker not running"; exit 1; }
    log_info "All tools are available"
}

fetch_repo() {
    mkdir -p "$DEPLOY_DIR"
    if [ -d "$DEPLOY_DIR/.git" ]; then
        log_info "Updating existing repository"
        cd "$DEPLOY_DIR" || exit 1
        git fetch origin
        git checkout main
        git pull origin main
    else
        log_info "Cloning repository"
        git clone "$REPO_LINK" "$DEPLOY_DIR" || { log_error "Clone failed"; exit 1; }
        cd "$DEPLOY_DIR" || exit 1
    fi
}

create_backup() {
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="${BACKUP_DIR}/${TIMESTAMP}"
    mkdir -p "$BACKUP_DIR"
    cp -r "$DEPLOY_DIR" "$BACKUP_FILE"
    log_info "Backup created at $BACKUP_FILE"
}

deploy_docker() {
    log_info "Building Docker image ${SERVICE}:${VER}"
    cd "$DEPLOY_DIR" || exit 1
    docker build -t "${SERVICE}:${VER}" . || { log_error "Docker build failed"; exit 1; }

    docker stop "${SERVICE}_cont" 2>/dev/null
    docker rm "${SERVICE}_cont" 2>/dev/null

    log_info "Starting container"
    docker run -d --name "${SERVICE}_cont" -p 8000:8000 -e ENV="$ENVIRON" -e VERSION="$VER" "${SERVICE}:${VER}" || { log_error "Container start failed"; exit 1; }
    sleep 5
}

check_health() {
    log_info "Checking service at http://localhost:8000/"
    CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)
    if [ "$CODE" = "200" ]; then
        log_info "Service is healthy (HTTP 200)"
        return 0
    else
        return 1
    fi
}

rollback_service() {
    log_error "Health check failed, performing rollback"
    docker stop "${SERVICE}_cont" 2>/dev/null
    docker rm "${SERVICE}_cont" 2>/dev/null

    if [ -d "$BACKUP_FILE" ]; then
        rm -rf "$DEPLOY_DIR"
        cp -r "$BACKUP_FILE" "$DEPLOY_DIR"
        log_info "Restored files from backup $BACKUP_FILE"
    else
        log_error "Backup not found, rollback impossible"
    fi

    REPORT="/tmp/${SERVICE}_report_$(date +%Y%m%d_%H%M%S).txt"
    {
        echo "Date: $(date)"
        echo "Service: $SERVICE"
        echo "Version: $VER"
        echo "Environment: $ENVIRON"
        echo "Backup: ${BACKUP_FILE:-not created}"
        echo "Reason: Health check failed"
    } > "$REPORT"
    log_error "Report saved at $REPORT"
}

main() {
    parse_args "$@"
    log_info "Deploying $SERVICE version $VER to $ENVIRON"

    check_dependencies
    fetch_repo
    create_backup
    deploy_docker

    if check_health; then
        exit 0
    else
        rollback_service
        exit 1
    fi
}

main "$@"


