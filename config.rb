
set :haml, format: :html5
set :css_dir, 'stylesheets'
set :js_dir, 'javascripts'
set :images_dir, 'images'

activate :s3_sync do |s|
  s.bucket = 'www.matthewekent.com'
  s.aws_access_key_id = ENV['AWS_ACCESS_KEY_ID']
  s.aws_secret_access_key = ENV['AWS_SECRET_ACCESS_KEY']
end