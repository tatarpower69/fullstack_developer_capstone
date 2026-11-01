# IBM Cloud Code Engine deployment

This is a deployment guide, not evidence that a cloud deployment has occurred.

Prerequisites: an authorized IBM Cloud account, Code Engine project, IBM Container Registry namespace, and a MongoDB service (TLS connection string). Do not paste account passwords or API keys into source files or Mark answers.

1. Build and push the web image using the root `Dockerfile`; build the dealers and sentiment images using their respective service Dockerfiles.
2. Deploy the dealers and sentiment services with private project visibility. Set `BIND_HOST=0.0.0.0`, `PORT=3030`, `MONGO_URL` and `SERVICE_TOKEN` on dealers. Keep MongoDB credentials in a Code Engine secret.
3. Deploy web on port 8000 with `DJANGO_DEBUG=0`, a secret `DJANGO_SECRET_KEY`, `SERVICE_TOKEN`, the two internal service URLs, the exact public hostname in `ALLOWED_HOSTS`, and its HTTPS origin in `CSRF_TRUSTED_ORIGINS`.
4. SQLite requires a persistent mounted filesystem and a single web replica. For reliable autoscaling replace SQLite with a managed PostgreSQL database; do not deploy SQLite on ephemeral storage and claim persistence.
5. Run migrations, seed the catalog, collect static files, and create the admin user through an authorized one-off job.
6. Test registration, login, a posted review, static pages, and logout at the real public URL. Capture tasks 24–28 only after this succeeds.

Kubernetes manifests are in `deploy/kubernetes.yaml`. Replace the three image placeholders, public hostname, and secret values using your actual environment. Internal services are not exposed publicly.
