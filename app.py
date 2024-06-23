import streamlit as st
import pandas as pd
import folium
from branca.element import Template, MacroElement
from streamlit_folium import st_folium

def display_map():
    map = folium.Map(
        location=[-3.539241, 118.941828],
        zoom_start=13,
        scrollWheelZoom=False,
    )

    data = pd.read_csv("banggae.csv")
    st.write(data.head())

    choropleth = folium.Choropleth(
        geo_data="banggae.json",
        data=data,
        columns=["DESA", "KEPADATAN"],
        key_on="feature.properties.DESA",
        fill_color="OrRd",
        fill_opacity=0.9,
        threshold_scale=[0, 3000, 5000, 7000, 11000],
        legend_name="Kepadatan",
    )

    choropleth.geojson.add_to(map)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(["DESA", "KEPADATAN"], labels=False),
    )

    map.save("index.html")
    macro = MacroElement()
    macro._template = Template(legend_template)
    map.get_root().add_child(macro)
    st_folium(map, width=700, height=450)

legend_template = """
{% macro html(this, kwargs) %}
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index: 9999; background-color: rgba(255, 255, 255, 0.5);
     border-radius: 6px; padding: 10px; font-size: 10.5px; right: 20px; top: 20px;'>     
<p style='margin: 0; padding-bottom: 5px; font-weight: bold; color: black; text-align: center;'>Kepadatan</p>
  
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background: #fcf3dc; opacity: 0.75;'></span>0.0 ~ 2999</li>
    <li><span style='background: #fbd193; opacity: 0.75;'></span>3.000 ~ 4.999</li>
    <li><span style='background: #fc9464; opacity: 0.75;'></span>5.000 ~ 6.999</li>
    <li><span style='background: #dc4434; opacity: 0.75;'></span>7.000 ~ 11.000</li>
  </ul>
</div>
</div> 
<style type='text/css'>
  .maplegend .legend-scale ul {margin: 0; padding: 0; color: #0f0f0f;}
  .maplegend .legend-scale ul li {list-style: none; line-height: 18px; margin-bottom: 1.5px;}
  .maplegend ul.legend-labels li span {float: left; height: 16px; width: 16px; margin-right: 4.5px;}
</style>
{% endmacro %}
"""

st.title("Peta Kepadatan Penduduk - Banggae, Majene, Sulawesi Barat")
display_map()
