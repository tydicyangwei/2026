## 常用的exporter

### 常用中间件和数据库的exporter镜像地址
mysqld_exporter prom/mysqld-exporter
postgres_exporter prometheuscommunity/postgres-exporter
redis_exporter oliver006/redis_exporter
etcd自带metrics
nginx-prometheus-exporter nginx/nginx-prometheus-exporter
Elasticsearch	prometheuscommunity/elasticsearch-exporter:latest	9114	社区标准，功能完善
MongoDB	percona/mongodb_exporter:0.40	9216	Percona 维护，功能最强
Kafka	confluentinc/kafka-exporter:latest	9308	Confluent 官方维护
RocketMQ	apache/rocketmq-exporter:latest	5557	Apache 官方组织镜像
minio 内置metrics /minio/v2/metrics/cluster

