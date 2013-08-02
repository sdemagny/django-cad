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
            bbox,
            cloudmade,
            osm,
            bing,
            mapbox,
            empty,

            ownership,
            parcels,
            lieudits,

            hash;

        config = $.extend(config, params);

        // zoomControl is false to enable zoomfs leaflet plugin
        map = L.map(config.mapdiv, {zoomControl: false}).setView(config.coord, 10);
        bbox = '-0.39, 45.2, -0.30, 45.25';

        hash = new L.Hash(map);

        empty = new L.Path();
        mapbox = new L.TileLayer('http://a.tiles.mapbox.com/v3/nippo.map-x23ct41d/{z}/{x}/{y}.png').addTo(map);
        cloudmade = L.tileLayer('http://{s}.tile.cloudmade.com/' + config.cloudmade_api_key + '/997/256/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; <a target="_blank"  href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a target="_blank"  href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a target="_blank"  href="http://cloudmade.com">CloudMade</a>',
            maxZoom: 18
        });
        osm = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {styleId: 999});
        bing = new L.BingLayer(config.bing_api_key, {});

        /** L.geoJson's, these calls load data from server */
        lieudits = IOS.l.edigeo.map.lieudits.get(bbox);
        ownership = IOS.l.cad.map.ownership.get(bbox);
        parcels = IOS.l.edigeo.map.parcels.get(bbox);


        $('#parcels').on('click', function () {
            if (map.hasLayer(parcels)) {
                parcels.removeLayer(parcels);
            } else {
                map.addLayer(parcels);
            }
        });

        $('#ownership').on('click', function () {
            if (map.hasLayer(ownership)) {
                ownership.removeLayer(ownership);
            } else {
                map.addLayer(ownership);
            }
        });

        $('#lieudits').on('click', function () {
            if (map.hasLayer(lieudits)) {
                lieudits.removeLayer(lieudits);
            } else {
                map.addLayer(lieudits);
            }
        });

        map.addControl(
            new L.Control.Layers(
                {
                    "Aucun": empty,
                    //"Bing": bing,
                    //'Cloudmade': cloudmade,
                    //"OSM": osm,
                    "Mapbox": mapbox
                },
                {
                    "Forêts privées": ownership,
                    "Lieudits": lieudits,
                    "Parcelles cadastrales": parcels
                },
                {}
            )
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


IOS.l.cad.map.ownership = (function (map) {
    'use strict';
    var config = {
            url: '/layers/cad/ownership',
            property: 'name',
            theme: 'theme',
            infos_container: '#infos'
        },
        get = function geojson(bbox) {
            var layer = L.geoJson('', {
                    style: function (feature) {

                        return {color: feature.properties[config.theme], weight: 1, opacity: 0.8};
                    },
                    onEachFeature: function onEachFeature(feature, layer) {
                        if (feature.properties && feature.properties[config.property]) {
                            $(layer).on('click mouseover', function (e) {
                                $(config.infos_container).html(feature.properties[config.property]);
                            });
                        }

                    },
                    attribution: '@todo'
                }),
                legend;
            $.getJSON(config.url + '?bbox=' + bbox, function (data) {
                $.each(data.features, function (index, element) {
                    layer.addData(element);
                });
            });

            return layer;
        };

    return {
        get: get
    };
}());
