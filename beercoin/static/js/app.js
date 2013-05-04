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
  factory("Profile", function($resource) {
    return $resource('/api/v1/profile/:profileId', {profileId:'@username'});
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
       when('/login', {controller:"LoginCtrl", templateUrl:'/accounts/signin/?next=/'}).
       when('/profile/:profileName', {controller:"ProfileCtrl", templateUrl:'/static/tmpl/profile.tmpl'}).
       // when('/edit/:projectId', {controller:EditCtrl, templateUrl:'detail.html'}).
      otherwise({redirectTo:'/'});
  }).
  controller ("ListCtrl", function ($scope, Profile, $location, appState) {
    // $scope.app_name = "My first angular App";
    $scope.profiles = Profile.query();
  }).
  controller ("LoginCtrl", function ($scope, $location, appState) {
    // $scope.app_name = "My first angular App";
    $scope.$on('$viewContentLoaded', function() {
      $("form").attr("action", "/accounts/signin/");

    });
  }).
  controller ("ProfileCtrl", function ($scope, Profile, $route, $location, appState) {
    $scope.profile = Profile.get({profileId: $route.current.params["profileName"]});
  }).
  controller ("MainCtrl", function ($scope, $location, appState) {
    console.log("yay");
    $scope.app_name = "My first angular App";
  }).run(function($location) {
    // checking for login and moving you to the login page if not
    $.getJSON("/api/v1/check_login", function(resp) {
      console.log(resp);
      if (!resp.success){
        document.location.href = "/accounts/signin/?next=/#" + $location.path();
      }
    });
  })
  ;
