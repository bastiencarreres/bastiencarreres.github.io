# This plugin defines a custom Liquid tag for Jekyll that fetches the citation count
# for a given NASA ADS bibcode using the NASA ADS API.
#
# Example usage in a Jekyll page:
#   {% nasa_ads_citations 2024ApJ...915..123A %}
#
# The plugin retrieves your ADS token from the environment variable `NASA_ADS_TOKEN`,
# so you do NOT have to expose it in your site source.
#
# Before building your site, make sure you have set:
#
# or if you use GitHub Actions, define it in repo secrets:
#   NASA_ADS_TOKEN: ${{ secrets.NASA_ADS_TOKEN }}

require 'net/http'
require 'json'
require 'uri'
require 'liquid'

module Jekyll
  class NasaADSCitationsTag < Liquid::Tag
    # A simple cache to avoid fetching the same citation count multiple times
    Citations = {}

    # Called when the tag is first parsed in the Liquid template
    def initialize(tag_name, params, tokens)
      super
      # Extract the bibcode passed as a parameter
      @bibcode = params.strip

      # Basic validation in case the tag is used incorrectly
      if @bibcode.nil? || @bibcode.empty?
        Jekyll.logger.warn "NASA ADS:", "No bibcode provided for nasa_ads_citations tag."
      end
    end

    # This method runs during site generation to replace the tag with its output
    def render(context)
      # Resolve the bibcode — it may be a literal or a Liquid variable
      bibcode = context[@bibcode.strip] || @bibcode.strip

      # Get the secret NASA ADS API token from the environment
      token = ENV['NASA_ADS_TOKEN']

      # If the token is not set, stop and show an error
      unless token
        Jekyll.logger.error "NASA ADS:", "Missing NASA_ADS_TOKEN environment variable."
        return "N/A"
      end

      # Use cached value if we already fetched this bibcode before
      if NasaADSCitationsTag::Citations[bibcode]
        return NasaADSCitationsTag::Citations[bibcode]
      end

      # Define the base NASA ADS API endpoint and query parameters
      base_url = "https://api.adsabs.harvard.edu/v1/search/query"
      query = URI.encode_www_form({
        q: "bibcode:#{bibcode}",  # search by bibcode
        fl: "citation_count"      # only request the citation count field
      })

      api_url = "#{base_url}?#{query}"

      begin
        # If the citation count has already been fetched, return it
        if NasaADSCitationsTag::Citations[bibcode]
          return NasaADSCitationsTag::Citations[bibcode]
        end

        # Build the HTTPS request
        uri = URI(api_url)
        req = Net::HTTP::Get.new(uri)
        req['Authorization'] = "Bearer #{token}"

        # Perform the request over HTTPS
        response = Net::HTTP.start(uri.hostname, uri.port, use_ssl: true) do |http|
          http.request(req)
        end

        # Parse the returned JSON data
        data = JSON.parse(response.body)
        puts data
        # Extract citation count from the first (and only) result document
        citation_count = data["response"]["docs"][0]["citation_count"].to_i

      rescue Exception => e
        # Handle any API or network errors gracefully
        citation_count = "N/A"
        Jekyll.logger.error "NASA ADS:", "Error fetching citation count for #{bibcode}: #{e.class} - #{e.message}"
      end

      # Cache the result for this build run to avoid repeated API calls
      NasaADSCitationsTag::Citations[bibcode] = citation_count

      # Return the citation count as a string to insert into the HTML
      return "#{citation_count}"
    end
  end
end

# Register this class as a new Liquid tag called `nasa_ads_citations`
Liquid::Template.register_tag('nasa_ads_citations', Jekyll::NasaADSCitationsTag)
