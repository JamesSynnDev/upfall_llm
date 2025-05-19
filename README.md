
### 배포 및 운영
1. 이미지 빌드 및 컨테이너 실행
   ```bash
    docker-compose -f docker-compose.yml build --no-cache web
    docker-compose -f docker-compose.yml up -d
    ```
2. 로그 확인
   ```bash
    docker-compose logs -f web
    docker-compose logs -f nginx
   ```
3. 도메인 및 SSL
   - Let's Encrypt / Certbot을 별도 컨테이너로 구성하거나, 
   - 호스트에서 인증서를 발급 후 Nginx에 마운트하여 HTTPS 설정을 추가
