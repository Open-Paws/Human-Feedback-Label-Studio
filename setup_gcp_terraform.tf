provider "google" {
  project     = "label-studio-424123"
  region      = "us-central1"
}

resource "google_project" "default" {
  auto_create_network = true
  billing_account     = "01DC86-694FD7-874183"
  folder_id           = null
  labels              = {}
  name                = "Label Studio"
  org_id              = jsonencode(115681881384)
  project_id          = "label-studio-424123"
  skip_delete         = null
}

resource "google_service_account" "default" {
  account_id                   = "label-studio-user"
  create_ignore_already_exists = null
  description                  = "A service account for running Label Studio, and related CI/CD"
  disabled                     = false
  display_name                 = "label-studio-user"
  project                      = "label-studio-424123"
}

# __generated__ by Terraform from "label-studio-424123 roles/logging.bucketWriter serviceAccount:label-studio-user@label-studio-424123.iam.gserviceaccount.com"
resource "google_project_iam_member" "bucketWriter" {
  member  = "serviceAccount:label-studio-user@label-studio-424123.iam.gserviceaccount.com"
  project = "label-studio-424123"
  role    = "roles/logging.bucketWriter"
}

# __generated__ by Terraform from "label-studio-424123 roles/secretmanager.secretAccessor serviceAccount:label-studio-user@label-studio-424123.iam.gserviceaccount.com"
resource "google_project_iam_member" "secretAccessor" {
  member  = "serviceAccount:label-studio-user@label-studio-424123.iam.gserviceaccount.com"
  project = "label-studio-424123"
  role    = "roles/secretmanager.secretAccessor"
}

# __generated__ by Terraform from "label-studio-424123 roles/cloudsql.client serviceAccount:label-studio-user@label-studio-424123.iam.gserviceaccount.com"
resource "google_project_iam_member" "cloudsql" {
  member  = "serviceAccount:label-studio-user@label-studio-424123.iam.gserviceaccount.com"
  project = "label-studio-424123"
  role    = "roles/cloudsql.client"
}

# __generated__ by Terraform from "label-studio-424123 roles/artifactregistry.repoAdmin serviceAccount:label-studio-user@label-studio-424123.iam.gserviceaccount.com"
resource "google_project_iam_member" "artifactregistry" {
  member  = "serviceAccount:label-studio-user@label-studio-424123.iam.gserviceaccount.com"
  project = "label-studio-424123"
  role    = "roles/artifactregistry.repoAdmin"
}

# __generated__ by Terraform from "label-studio-424123 roles/logging.logWriter serviceAccount:label-studio-user@label-studio-424123.iam.gserviceaccount.com"
resource "google_project_iam_member" "logWriter" {
  member  = "serviceAccount:label-studio-user@label-studio-424123.iam.gserviceaccount.com"
  project = "label-studio-424123"
  role    = "roles/logging.logWriter"
}

# __generated__ by Terraform from "label-studio-424123 roles/iam.serviceAccountTokenCreator serviceAccount:label-studio-user@label-studio-424123.iam.gserviceaccount.com"
resource "google_project_iam_member" "serviceAccountTokenCreator" {
  member  = "serviceAccount:label-studio-user@label-studio-424123.iam.gserviceaccount.com"
  project = "label-studio-424123"
  role    = "roles/iam.serviceAccountTokenCreator"
}

# __generated__ by Terraform from "label-studio-424123 roles/storage.admin serviceAccount:label-studio-user@label-studio-424123.iam.gserviceaccount.com"
resource "google_project_iam_member" "storage" {
  member  = "serviceAccount:label-studio-user@label-studio-424123.iam.gserviceaccount.com"
  project = "label-studio-424123"
  role    = "roles/storage.admin"
}

resource "google_sql_database_instance" "default" {
  database_version     = "POSTGRES_15"
  deletion_protection  = true
  encryption_key_name  = null
  instance_type        = "CLOUD_SQL_INSTANCE"
  maintenance_version  = "POSTGRES_15_7.R20240514.00_04"
  master_instance_name = null
  name                 = "label-studio-postgres"
  project              = "label-studio-424123"
  region               = "us-central1"
  root_password        = null # sensitive
  settings {
    activation_policy            = "ALWAYS"
    availability_type            = "ZONAL"
    collation                    = null
    connector_enforcement        = "NOT_REQUIRED"
    deletion_protection_enabled  = true
    disk_autoresize              = true
    disk_autoresize_limit        = 0
    disk_size                    = 20
    disk_type                    = "PD_SSD"
    edition                      = "ENTERPRISE"
    enable_google_ml_integration = false
    pricing_plan                 = "PER_USE"
    tier                         = "db-custom-2-8192"
    time_zone                    = null
    user_labels                  = {}
    backup_configuration {
      binary_log_enabled             = false
      enabled                        = true
      location                       = "us"
      point_in_time_recovery_enabled = true
      start_time                     = "21:00"
      transaction_log_retention_days = 4
      backup_retention_settings {
        retained_backups = 4
        retention_unit   = "COUNT"
      }
    }
    insights_config {
      query_insights_enabled  = true
      query_plans_per_minute  = 5
      query_string_length     = 1024
      record_application_tags = false
      record_client_address   = false
    }
    ip_configuration {
      allocated_ip_range                            = null
      enable_private_path_for_google_cloud_services = false
      ipv4_enabled                                  = true
      private_network                               = null
      ssl_mode                                      = null
    }
    location_preference {
      follow_gae_application = null
      secondary_zone         = null
      zone                   = "us-central1-c"
    }
    maintenance_window {
      day          = 1
      hour         = 1
      update_track = null
    }
  }
}

resource "google_sql_database" "default" {
  charset         = "UTF8"
  collation       = "en_US.UTF8"
  deletion_policy = "DELETE"
  instance        = "label-studio-postgres"
  name            = "postgres"
  project         = "label-studio-424123"
}

resource "google_artifact_registry_repository" "default" {
  cleanup_policy_dry_run = true
  description            = "images for Label Studio's container"
  format                 = "DOCKER"
  kms_key_name           = null
  labels                 = {}
  location               = "us-central1"
  mode                   = "STANDARD_REPOSITORY"
  project                = "label-studio-424123"
  repository_id          = "label-studio"
  docker_config {
    immutable_tags = false
  }
}

resource "google_storage_bucket" "default2" {
  default_event_based_hold    = false
  enable_object_retention     = false
  force_destroy               = false
  labels                      = {}
  location                    = "US"
  name                        = "label-studio-input-open-paws"
  project                     = "label-studio-424123"
  public_access_prevention    = "enforced"
  requester_pays              = false
  rpo                         = "DEFAULT"
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  soft_delete_policy {
    retention_duration_seconds = 604800
  }
}

# __generated__ by Terraform from "label-studio-424123/label-studio-output"
resource "google_storage_bucket" "default1" {
  default_event_based_hold    = false
  enable_object_retention     = false
  force_destroy               = false
  labels                      = {}
  location                    = "US"
  name                        = "label-studio-output"
  project                     = "label-studio-424123"
  public_access_prevention    = "enforced"
  requester_pays              = false
  rpo                         = "DEFAULT"
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  soft_delete_policy {
    retention_duration_seconds = 604800
  }
}

resource "google_cloud_run_v2_service" "default" {
  annotations      = {}
  client           = "cloud-console"
  client_version   = null
  custom_audiences = []
  description      = null
  ingress          = "INGRESS_TRAFFIC_ALL"
  labels           = {}
  launch_stage     = "BETA"
  location         = "us-central1"
  name             = "human-feedback-label-studio"
  project          = "label-studio-424123"
  template {
    annotations                      = {}
    encryption_key                   = null
    execution_environment            = null
    labels                           = {}
    max_instance_request_concurrency = 80
    revision                         = null
    service_account                  = "label-studio-user@label-studio-424123.iam.gserviceaccount.com"
    session_affinity                 = false
    timeout                          = "300s"
    containers {
      args        = []
      command     = []
      depends_on  = []
      image       = "us-central1-docker.pkg.dev/label-studio-424123/label-studio/label-studio:latest"
      name        = "placeholder-1"
      working_dir = null
      env {
        name  = "USERNAME"
        value = "sam@veg3.ai"
      }
      env {
        name  = "PASSWORD"
        value = "Op3np@ws1234"
      }
      env {
        name  = "DISABLE_SIGNUP_WITHOUT_LINK"
        value = jsonencode(0)
      }
      env {
        name  = "DJANGO_DB"
        value = "default"
      }
      env {
        name  = "POSTGRE_NAME"
        value = "postgres"
      }
      env {
        name  = "POSTGRE_USER"
        value = "postgres"
      }
      env {
        name  = "POSTGRE_HOST"
        value = "/cloudsql/label-studio-424123:us-central1:label-studio-postgres"
      }
      env {
        name  = "POSTGRE_PORT"
        value = jsonencode(5432)
      }
      env {
        name  = "POSTGRE_PASSWORD"
        value = null
        value_source {
          secret_key_ref {
            secret  = "label-studio-postgres-admin"
            version = "latest"
          }
        }
      }
      ports {
        container_port = 8080
        name           = "http1"
      }
      resources {
        cpu_idle = true
        limits = {
          cpu    = "1000m"
          memory = "512Mi"
        }
        startup_cpu_boost = true
      }
      startup_probe {
        failure_threshold     = 1
        initial_delay_seconds = 0
        period_seconds        = 240
        timeout_seconds       = 240
        tcp_socket {
          port = 8080
        }
      }
      volume_mounts {
        mount_path = "/cloudsql"
        name       = "cloudsql"
      }
    }
    scaling {
      max_instance_count = 100
      min_instance_count = 0
    }
    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = ["label-studio-424123:us-central1:label-studio-postgres"]
      }
    }
  }
  traffic {
    percent  = 100
    revision = null
    tag      = null
    type     = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
  }
}
