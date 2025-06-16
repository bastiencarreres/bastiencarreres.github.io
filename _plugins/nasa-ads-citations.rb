require "active_support/all"
require 'net/http'
require 'json'
require 'uri'

module Jekyll
  class NasaADSCitationsTag < Liquid::Tag
    Citations = { }

    def initialize(tag_name, params, tokens)
      super
      splitted = params.split(" ").map(&:strip)
      @token = splitted[0]
      @bibcode = splitted[1]

      if @token.nil? || @token.empty?
        puts "Invalid token provided"
      end

      if @bibcode.nil? || @bibcode.empty?
        puts "Invalid bibcode provided"
      end
    end

    def render(context)
      bibcode = context[@bibcode.strip]
      token = context[@token.strip]

      base_url = "https://api.adsabs.harvard.edu/v1/search/query"
      query = URI.encode_www_form({
        q: "bibcode:#{bibcode}",
        fl: "citation_count"
        })
        
      api_url = "#{base_url}?#{query}"

      begin
        # If the citation count has already been fetched, return it
        if NasaADSCitationsTag::Citations[bibcode]
          return NasaADSCitationsTag::Citations[bibcode]
        end

        uri = URI(api_url)
        req = Net::HTTP::Get.new(uri)
        req['Authorization'] = "Bearer #{token}"

        response = Net::HTTP.start(uri.hostname, uri.port, use_ssl: true) do |http|
          http.request(req)
        end

        data = JSON.parse(response.body)

        citation_count = data["response"]["docs"][0]["citation_count"].to_i

      rescue Exception => e
        # Handle any errors that may occur during fetching
        citation_count = "N/A"

        # Print the error message including the exception class and message
        puts "Error fetching citation count for #{recid}: #{e.class} - #{e.message}"
      end

      NasaADSCitationsTag::Citations[bibcode] = citation_count
      return "#{citation_count}"
    end
  end
end

Liquid::Template.register_tag('nasa_ads_citations', Jekyll::NasaADSCitationsTag)
