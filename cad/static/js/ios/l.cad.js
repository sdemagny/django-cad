/*jslint browser: true*/
/*global $, jQuery, IOS, L*/

IOS.ns('l.cad.map');

IOS.l.cad.map = (function () {
    'use strict';

    var config = {
            coord: [48.833349, 2.289649],
            mapdiv: 'map'
        };

    function initMap(params) {
        var map,
            cloudmade,
            osm,
            bing,
            mapbox,
            parcels,
            lieudits,
            edigeo;

        config = $.extend(config, params);

        // zoomControl is false to enable zoomfs leaflet plugin
        map = L.map(config.mapdiv, {zoomControl: false}).setView(config.coord, 10);

        mapbox = new L.TileLayer('http://a.tiles.mapbox.com/v3/nippo.map-x23ct41d/{z}/{x}/{y}.png').addTo(map);
        cloudmade = L.tileLayer('http://{s}.tile.cloudmade.com/' + config.cloudmade_api_key + '/997/256/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; <a target="_blank"  href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a target="_blank"  href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a target="_blank"  href="http://cloudmade.com">CloudMade</a>',
            maxZoom: 18
        });
        osm = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {styleId: 999});
        bing = new L.BingLayer(config.bing_api_key, {});

        /** L.geoJson's, these calls load data from server */
        lieudits = IOS.l.edigeo.map.lieudits.get();
        parcels = IOS.l.cad.map.parcels.get();
        edigeo = IOS.l.edigeo.map.parcelles.get();

        map.addControl(
            new L.Control.Layers({"Bing": bing, 'Cloudmade': cloudmade, "OSM": osm, "Mapbox": mapbox}, {
                "Forêts privées": parcels,
                "Lieudits": lieudits,
                "Parcelles cadastrales": edigeo
            }, {})
        );

        map.addControl(new L.Control.ZoomFS());
        map.addControl(new L.Control.Scale());
        map.attributionControl.setPrefix('');

        return map;
    }

    return {
        initMap: initMap
    };
}());


IOS.l.cad.map.parcels = (function () {
    'use strict';
    var config = {
            url: '/layers/cad/parcels',
            property: 'code_edigeo'
        },
        geojson = function geojson() {
            var layer = L.geoJson('', {
                    onEachFeature: function onEachFeature(feature, layer) {
                        if (feature.properties && feature.properties[config.property]) {
                            layer.bindPopup(feature.properties[config.property]);
                        }
                    },
                    attribution: '@todo'
                }),
                legend;
            $.getJSON(config.url, function (data) {
                $.each(data.features, function (index, element) {
                    layer.addData(element);
                });
            });

            return layer;
        };

    return {
        get: geojson
    };
}());
