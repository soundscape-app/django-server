FROM arm64v8/nginx

# timezone 설정
# RUN apk add tzdata \
#     && cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime \
#     && echo "Asia/Seoul" > /etc/timezone \
#     && apk del tzdata
ENV TZ="Asia/Seoul"

RUN rm -r /etc/nginx/conf.d
COPY ./docker/nginx/nginx.conf /etc/nginx/
EXPOSE 80