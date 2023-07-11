# Helm

If you have access to a Kubernetes cluster and Helm, feel free to helm install the `values.yaml` listed here which utilizes the [bitnami mongodb helm chart](https://artifacthub.io/packages/helm/bitnami/mongodb) 


## Getting Started

1. `helm install mongodb oci://registry-1.docker.io/bitnamicharts/mongodb --values values.yaml`