angular.module('app.services', ['ngResource', 'ui']).
  directive('twModal', function() {
    return {
      scope: true,
      link: function(scope, element, attr, ctrl) {
          scope.show = function() {
            $(element).modal("show");
          };
          scope.dismiss = function() {
            $(element).modal("hide");
          };
          $(element).on("show", function(){
            scope.$emit("modalShow", arguments);
          });
          $(element).on("shown", function(){
            scope.$emit("modalShown", arguments);
          });
          $(element).on("hide", function(){
            scope.$emit("modalHide", arguments);
          });
          $(element).on("hidden", function(){
            scope.$emit("modalHidden", arguments);
          });
        }
      };
  }).
  directive('editable', function() {
    return {
      require: 'ngModel',
      link: function(scope, elm, attrs, model) {
        elm.editable(scope.$eval(attrs.editable));
        model.$render = function() {
            elm.editable('setValue', model.$viewValue);
        };
        elm.on('save', function(e, params) {
            model.$setViewValue(params.newValue);
            scope.$apply();
        });
        if (attrs.editableSaved) {
          elm.on('save', function(){
            scope.$eval(attrs.editableSaved);
           });
        }
      }
    };
  }).
  service('appState', function(){

  });

var crowdbetApp = angular.module('app', ["app.services"]).
  config(function($routeProvider) {
     $routeProvider.
       when('/', {controller:"MainCtrl", templateUrl:'/static/tmpl/main.tmpl'}).
       when('/list', {controller:"ListCtrl", templateUrl:'/static/tmpl/list.tmpl'}).
       when('/login', {controller:"LoginCtrl", templateUrl:'/static/tmpl/login.tmpl'}).
       when('/profile', {controller:"ProfileCtrl", templateUrl:'/static/tmpl/profile.tmpl'}).
       // when('/edit/:projectId', {controller:EditCtrl, templateUrl:'detail.html'}).
      otherwise({redirectTo:'/'});
  }).
  controller ("ListCtrl", function ($scope, $location, appState) {
    // $scope.app_name = "My first angular App";
  }).
  controller ("LoginCtrl", function ($scope, $location, appState) {
    // $scope.app_name = "My first angular App";
  }).
  controller ("ProfileCtrl", function ($scope, $location, appState) {
    // $scope.app_name = "My first angular App";
  }).
  controller ("MainCtrl", function ($scope, $location, appState) {
    console.log("yay");
    $scope.app_name = "My first angular App";
  });
