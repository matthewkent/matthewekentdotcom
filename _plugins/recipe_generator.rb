module Jekyll
  class RecipePage < Page
    def initialize(site, base, dir, name, recipe_name, recipe_data)
      super(site, base, dir, name)
      self.data["permalink"] = "/recipes/#{recipe_name}.html"
      recipe_data.each do |k, v|
        self.data[k] = v
      end
    end
  end

  class RecipePageGenerator < Generator
    safe true

    def generate(site)
      data_dir = File.expand_path("../recipe_data", File.dirname(__FILE__))
      Dir.glob("#{data_dir}/*.yaml").each do |f|
        recipe_data = YAML.load_file(f)
        site.pages << RecipePage.new(site, site.source, "", "recipe.html", File.basename(f, ".yaml"), recipe_data)
      end
    end
  end
end
