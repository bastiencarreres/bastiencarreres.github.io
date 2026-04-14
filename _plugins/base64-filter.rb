require 'base64'

module Jekyll
  module Base64Filter
    def base64_encode(input)
      Base64.strict_encode64(input)
    end
  end
end

Liquid::Template.register_filter(Jekyll::Base64Filter)
