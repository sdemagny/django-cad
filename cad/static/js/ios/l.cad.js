/*jslint browser: true*/
/*global $, jQuery, IOS, L, gettext*/

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
            mapbox,
            empty,
            bing,

            ownership,
            parcels,
            lieudits,

            hash;

        config = $.extend(config, params);

        map = L.map(config.mapdiv, {}).setView(config.coord, 10);

        L.control.fullscreen({
            position: 'topleft',
            title: gettext('Fullscreen')
        }).addTo(map);

        bbox = '-0.39, 45.2, -0.30, 45.25';

        hash = new L.Hash(map);

        empty = new L.Path().addTo(map);
        mapbox = new L.TileLayer('http://a.tiles.mapbox.com/v3/nippo.map-x23ct41d/{z}/{x}/{y}.png');
        bing = new L.BingLayer(config.bing_api_key, {});

        /** L.geoJson's, these calls load data from server */
        lieudits = IOS.l.edigeo.map.lieudits.get(bbox);
        parcels = IOS.l.edigeo.map.parcels.get(bbox);
        ownership = IOS.l.cad.map.ownership.get(bbox).addTo(map);

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
                    "Bing": bing,
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
