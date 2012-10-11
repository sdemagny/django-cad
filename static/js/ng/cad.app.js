/*jslint browser: true*/
/*global $, jQuery, IOS, L*/
'use strict';

var angular = angular || {},
    ArticleListCtrl,
    ArticleDetailCtrl,
    ArticleMapCtrl;

angular.module('ios', ['iosFilters', 'iosServices']).config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/parcels',
        {templateUrl: 'partials/cad.list.html',   controller: ArticleListCtrl})
            .otherwise({redirectTo: '/parcels'});
}]);

/* Controllers */

function ArticleListCtrl($scope, Article) {
    $scope.articles = Article.query();
    $scope.orderProp = 'id';
}

function ArticleMapCtrl($scope, $routeParams, Article) {

    $scope.articles = Article.query();
    $scope.orderProp = 'id';
}

/* Filters */

angular.module('iosFilters', []).filter('dosomething', function () {

    return function (input) {

        return input ? '\u2713' : '\u2718';
    };
});

/* Services */

angular.module('iosServices', ['ngResource']).factory('Article', function ($resource) {

    /* This resources aren't static */
    return $resource('data/cad/:articleId.json', {}, {
        query: {method: 'GET', params: {articleId: 'articles'}, isArray: false}
    });
});
