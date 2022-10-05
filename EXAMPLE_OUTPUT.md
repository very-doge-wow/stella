
# kibana
![Version: 8.4.1](https://img.shields.io/badge/Version-8.4.1-informational?style=flat-square) ![Version: 8.4.1](https://img.shields.io/badge/appVersion-8.4.1-informational?style=flat-square) ![Version: v1](https://img.shields.io/badge/apiVersion-v1-informational?style=flat-square) ![Type: unknown](https://img.shields.io/badge/Type-unknown-informational?style=flat-square) 

## Description
Official Elastic helm chart for Kibana

## Dependencies
This chart depends on the following subcharts.

*No dependencies found.*

## Templates
The following templates will be deployed.

| Path |
|---| 
| configmap-helm-scripts.yaml |
| configmap.yaml |
| deployment.yaml |
| ingress.yaml |
| job.yaml |
| service.yaml |


### Objects
The aforementioned templates will deploy the following objects.

| Kind | From template |
|---|---| 
| ConfigMap | configmap-helm-scripts.yaml |
| ConfigMap | configmap.yaml |
| Deployment | deployment.yaml |
| Ingress | ingress.yaml |
| Job | job.yaml |
| Service | service.yaml |


## Values
The following values can/will be used for deployments.

| Name | Description | Default | Example |
|---|---|---|---| 
| elasticsearchHosts |  | <pre>elasticsearchHosts: https://elasticsearch-master:9200<br></pre> |  |
| elasticsearchCertificateSecret |  | <pre>elasticsearchCertificateSecret: elasticsearch-master-certs<br></pre> |  |
| elasticsearchCertificateAuthoritiesFile |  | <pre>elasticsearchCertificateAuthoritiesFile: ca.crt<br></pre> |  |
| elasticsearchCredentialSecret |  | <pre>elasticsearchCredentialSecret: elasticsearch-master-credentials<br></pre> |  |
| replicas |  | <pre>replicas: 1<br></pre> |  |
| extraEnvs |  | <pre>extraEnvs:<br>- name: NODE_OPTIONS<br>  value: --max-old-space-size=1800<br></pre> |  |
| envFrom |  | <pre>envFrom: []<br></pre> |  |
| secretMounts |  | <pre>secretMounts: []<br></pre> |  |
| hostAliases |  | <pre>hostAliases: []<br></pre> |  |
| image |  | <pre>image: docker.elastic.co/kibana/kibana<br></pre> |  |
| imageTag |  | <pre>imageTag: 8.4.1<br></pre> |  |
| imagePullPolicy |  | <pre>imagePullPolicy: IfNotPresent<br></pre> |  |
| labels |  | <pre>labels: {}<br></pre> |  |
| annotations |  | <pre>annotations: {}<br></pre> |  |
| podAnnotations |  | <pre>podAnnotations: {}<br></pre> |  |
| resources |  | <pre>resources:<br>  limits:<br>    cpu: 1000m<br>    memory: 2Gi<br>  requests:<br>    cpu: 1000m<br>    memory: 2Gi<br></pre> |  |
| protocol |  | <pre>protocol: http<br></pre> |  |
| serverHost |  | <pre>serverHost: 0.0.0.0<br></pre> |  |
| healthCheckPath |  | <pre>healthCheckPath: /app/kibana<br></pre> |  |
| kibanaConfig |  | <pre>kibanaConfig: {}<br></pre> |  |
| podSecurityContext |  | <pre>podSecurityContext:<br>  fsGroup: 1000<br></pre> |  |
| securityContext |  | <pre>securityContext:<br>  capabilities:<br>    drop:<br>    - ALL<br>  runAsNonRoot: true<br>  runAsUser: 1000<br></pre> |  |
| serviceAccount |  | <pre>serviceAccount: ''<br></pre> |  |
| automountToken |  | <pre>automountToken: true<br></pre> |  |
| priorityClassName |  | <pre>priorityClassName: ''<br></pre> |  |
| httpPort |  | <pre>httpPort: 5601<br></pre> |  |
| extraVolumes |  | <pre>extraVolumes: []<br></pre> |  |
| extraVolumeMounts |  | <pre>extraVolumeMounts: []<br></pre> |  |
| extraContainers |  | <pre>extraContainers: []<br></pre> |  |
| extraInitContainers |  | <pre>extraInitContainers: []<br></pre> |  |
| updateStrategy |  | <pre>updateStrategy:<br>  type: Recreate<br></pre> |  |
| service |  | <pre>service:<br>  annotations: {}<br>  httpPortName: http<br>  labels: {}<br>  loadBalancerIP: ''<br>  loadBalancerSourceRanges: []<br>  nodePort: ''<br>  port: 5601<br>  type: ClusterIP<br></pre> |  |
| ingress |  | <pre>ingress:<br>  annotations: {}<br>  className: nginx<br>  enabled: false<br>  hosts:<br>  - host: kibana-example.local<br>    paths:<br>    - path: /<br>  pathtype: ImplementationSpecific<br></pre> |  |
| readinessProbe |  | <pre>readinessProbe:<br>  failureThreshold: 3<br>  initialDelaySeconds: 10<br>  periodSeconds: 10<br>  successThreshold: 3<br>  timeoutSeconds: 5<br></pre> |  |
| imagePullSecrets |  | <pre>imagePullSecrets: []<br></pre> |  |
| nodeSelector |  | <pre>nodeSelector: {}<br></pre> |  |
| tolerations |  | <pre>tolerations: []<br></pre> |  |
| affinity |  | <pre>affinity: {}<br></pre> |  |
| nameOverride |  | <pre>nameOverride: ''<br></pre> |  |
| fullnameOverride |  | <pre>fullnameOverride: ''<br></pre> |  |
| lifecycle |  | <pre>lifecycle: {}<br></pre> |  |


*Automatic helm documentation generated using [very-doge-wow/stella](https://github.com/very-doge-wow/stella).*

