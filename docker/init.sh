#!/bin/bash

if [ -d "/home/frappe/frappe-bench/apps/frappe" ]; then
    echo "Bench already exists, skipping init"
    cd frappe-bench
    bench start
else
    echo "Creating new bench..."
    
    bench init --skip-redis-config-generation frappe-bench
    cd frappe-bench
    
    # Use containers instead of localhost for MariaDB and Redis
    bench set-mariadb-host mariadb
    bench set-redis-cache-host redis://redis:6379
    bench set-redis-queue-host redis://redis:6379
    bench set-redis-socketio-host redis://redis:6379
    
    # Remove redis and watch processes from Procfile to avoid conflicts
    sed -i '/redis/d' ./Procfile
    sed -i '/watch/d' ./Procfile
    
    # Get ERPNext and HRMS apps
    bench get-app erpnext
    bench get-app hrms
    
    # Create new site with environment-provided passwords
    bench new-site hrms.localhost \
      --force \
      --mariadb-root-password ${MYSQL_ROOT_PASSWORD} \
      --admin-password ${ADMIN_PASSWORD} \
      --no-mariadb-socket
    
    # Install HRMS app
    bench --site hrms.localhost install-app hrms
    
    # Enable developer mode and scheduler, clear cache
    bench --site hrms.localhost set-config developer_mode 1
    bench --site hrms.localhost enable-scheduler
    bench --site hrms.localhost clear-cache
    
    # Use the new site by default
    bench use hrms.localhost
    
    # Finally start bench
    bench start
fi
