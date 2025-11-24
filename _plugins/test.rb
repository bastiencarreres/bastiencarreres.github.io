require 'net/http'
require 'json'
require 'uri'
require 'liquid'
require_relative 'nasa-ads-citations'  # path to your plugin


# Example bibcode to test
bibcode = "2025arXiv250513290C"

# Define a simple Liquid template that uses your custom tag
template = Liquid::Template.parse("{% nasa_ads_citations #{bibcode} %}")

# Render the template (no Jekyll needed)
puts "Fetching citation count for #{bibcode}..."
output = template.render({}, registers: { :site => nil })
puts "Output: #{output}"
