module Jekyll
  class DataPage < Page
    def initialize(site, base, dir, name, extra_data)
      super(site, base, dir, name)
      extra_data.each do |k, v|
        self.data[k] = v
      end
    end
  end

  class RecipePageGenerator < Generator
    safe true

    def generate(site)
      data_dir = File.expand_path("../recipe_data", File.dirname(__FILE__))
      recipe_links = {}
      Dir.glob("#{data_dir}/*.yaml").each do |f|
        recipe_data = YAML.load_file(f)
        recipe_permalink = "/recipes/#{File.basename(f, ".yaml")}.html"
        recipe_links[recipe_data["title"]] = recipe_permalink
        site.pages << DataPage.new(site, site.source, "", "recipe_view.html", recipe_data.merge("permalink" => recipe_permalink))
      end
      site.pages << DataPage.new(site, site.source, "", "recipe_index.html", {"recipe_links" => recipe_links})
    end
  end
end
