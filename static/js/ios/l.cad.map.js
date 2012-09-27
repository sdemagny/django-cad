/*jslint browser: true*/
/*global $, jQuery, IOS, L*/

IOS.ns('l.cad.map');

IOS.l.cad.map = (function () {
    'use strict';

    var config = {
            coord: [48.833349, 2.289649],
            mapdiv: 'frt-map'
        };

    function init(params) {
        var parcels,
            lieudits,
            map,
            marker,
            cloudmade,
            osm,
            bing,
            d,
            z,
            data,
            geojsonFeature,
            mapbox,
            geocoder;

        config = $.extend(config, params);

        map = L.map(config.mapdiv, {zoomControl: false}).setView(config.coord, 10);

        mapbox = new L.TileLayer('http://a.tiles.mapbox.com/v3/nippo.map-x23ct41d/{z}/{x}/{y}.png').addTo(map);
        cloudmade = L.tileLayer('http://{s}.tile.cloudmade.com/' + config.cloudmade_api_key + '/997/256/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; <a target="_blank"  href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a target="_blank"  href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a target="_blank"  href="http://cloudmade.com">CloudMade</a>',
            maxZoom: 18
        });
        osm = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {styleId: 999});
        bing = new L.BingLayer(config.bing_api_key, {});


        lieudits = IOS.l.cad.map.lieudits.get();
        parcels = IOS.l.cad.map.parcels.get();

        map.addControl(new L.Control.Layers({"Bing": bing, 'Cloudmade': cloudmade, "OSM": osm, "Mapbox": mapbox}, {"Parcelles cadastrales": parcels, "Lieudit": lieudits}, {}));
        d = new L.Control.Distance();
        map.addControl(d);
        map.addControl(new L.Control.Permalink({useLocation: true}));
        map.addControl(new L.Control.Scale());
        map.addControl(new L.Control.ZoomFS());
        geocoder = new L.Control.BingGeocoder(config.bing_api_key);
        map.addControl(geocoder);
    }

    return {
        init: init
    };
}());


IOS.ns('l.cad.map.parcels');


IOS.l.cad.map.parcels = (function () {
    'use strict';
    var tiles = function tiles() {
        var parcels = L.geoJson();
        $.getJSON('/layers/cad/prc', function (data) {
            $.each(data.features, function (index, element) {
                parcels.addData(element);
            });
        });

        return parcels;
    };

    return {
        get: tiles
    };
}());

IOS.ns('l.cad.map.lieudits');


IOS.l.cad.map.lieudits = (function () {
    'use strict';
    var tiles = function tiles() {
        var lieudits = L.geoJson();
        $.getJSON('/layers/edigeo/lieudit', function (data) {
            var index;
            $.each(data.features, function (index, element) {
                lieudits.addData(element);
            });
        });

        return lieudits;
    };

    return {
        get: tiles
    };
}());
