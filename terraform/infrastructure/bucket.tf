resource "google_storage_bucket" "public_bucket" {
  name          = "dynamic-hotel-public-bucket"
  location      = "US"
  force_destroy = true

  uniform_bucket_level_access = true

  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }
}

resource "google_storage_bucket_iam_binding" "public_access" {
  bucket = google_storage_bucket.public_bucket.name

   role   = "roles/storage.objectViewer"
  members = [
    "allUsers",
  ]
}