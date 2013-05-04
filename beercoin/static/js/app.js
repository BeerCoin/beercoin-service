angular.module('app.services', ['ngResource', 'ui']).
  filter("since", function(){
    return function(date){
      return moment(date).fromNow();
    };
  }).
  factory('pusher', function() {
    var pusher = new Pusher('20adaedfdf8be72a2ed9');
    return pusher;
  }).
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
  	return {
  		loggedIn: false
  	};
  });

var crowdbetApp = angular.module('app', ["app.services"]).
  config(function($routeProvider) {
     $routeProvider.
       when('/', {controller:"MainCtrl", templateUrl:'/static/tmpl/main.tmpl'}).
       when('/login', {controller:"LoginCtrl", templateUrl:'/accounts/signin/?next=/'}).
       when('/profiles', {controller:"ListCtrl", templateUrl:'/static/tmpl/profiles.tmpl'}).
       when('/profile/:profileName', {controller:"ProfileCtrl", templateUrl:'/static/tmpl/profile.tmpl'}).
       // when('/edit/:projectId', {controller:EditCtrl, templateUrl:'detail.html'}).
      otherwise({redirectTo:'/'});
  }).
  controller ("ListCtrl", function ($scope, Profile, $location, appState) {
    // maybe we want to filter these some time
    $scope.profiles = Profile.query();
    $scope.search = {location:"", balance:0 };
    $scope.searcher = function(item) {
    	if (!$scope.search.location ||
			($scope.search.location && item.location.toLowerCase().indexOf($scope.search.location.toLowerCase()) > -1) ) {
    		
    		if (!$scope.search.balance || $scope.search.balance==0 ||
    			($scope.search.balance==1 && item.balance>0) || 
    			($scope.search.balance==2 && item.balance<=0) ) {
		    		return true;
    			}
    	}
    }
    appState.loggedIn = true;
  }).
  controller ("LoginCtrl", function ($scope, $location, appState) {
    $scope.$on('$viewContentLoaded', function() {
      $("form").attr("action", "/accounts/signin/");
    });
  }).
  controller ("ProfileCtrl", function ($scope, Profile, $route, $location, appState) {
    $scope.profile = Profile.get({profileId: $route.current.params["profileName"]});
    $scope.appState = appState;
    appState.loggedIn = true;
    $scope.issue = function() {
      // FIXME: disable button
      $.getJSON("/api/v1/beercoin/issue?owner=" + $scope.profile.username, function(res) {
        if (res.error) {
        	$('#thankYouModal .modal-body P').html(res.message);
        	$('#thankYouModal').modal();
          return;
        }
        var pf_name = $scope.profile.name;
        $scope.profile = Profile.get({profileId: $route.current.params["profileName"]});
       	$('#thankYouModal .modal-body P').html(pf_name + " says thanks. You are awesome!");
       	$('#thankYouModal').modal();
      });
    };
    $scope.redeem = function() {
      // FIXME: disable button
      $.getJSON("/api/v1/beercoin/redeem?issuer=" + $scope.profile.username, function(res) {
        if (res.error) {
        	$('#thankYouModal .modal-body P').html(res.message);
        	$('#thankYouModal').modal();
          return;
        }
        var pf_name = $scope.profile.name;
        $scope.profile = Profile.get({profileId: $route.current.params["profileName"]});
       	$('#thankYouModal .modal-body P').html(pf_name + " was happy to help. You are awesome!");
       	$('#thankYouModal').modal();
      });
    };

    $scope.ask = function() {
      // FIXME: disable button
      $.getJSON("/api/v1/social/ask?user=" + $scope.profile.username, function(res) {
        if (res.error) {
          alert(res.message);
          return;
        }
        var pf_name = $scope.profile.name;
        $scope.profile = Profile.get({profileId: $route.current.params["profileName"]});
        alert(pf_name + " received your message.");
      });
    };
  }).
  controller ("OuterCtrl", function ($scope, $location, appState){
  	$scope.appState = appState;
  }).
  controller ("MainCtrl", function ($scope, $location, appState) {
    $scope.app_name = "My first angular App";
    appState.loggedIn = true;
  }).run(function($location, pusher, appState) {
    // checking for login and moving you to the login page if not
    $.getJSON("/api/v1/check_login", function(resp) {
      appState.user = resp.user;
      if (!resp.success){
        document.location.href = "/accounts/signin/?next=/#" + $location.path();
      }

      var channel = pusher.subscribe('user_' + appState.user.username);
      channel.bind('msg', function(data) {
        alert(data);
      });
    });
  })
  ;
