source version
docker tag pumpwood-auth-static:${VERSION} andrebaceti/micropython-backend-static:${VERSION}
gcloud docker -- push andrebaceti/micropython-backend-static:${VERSION}
