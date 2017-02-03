(function () {

  // login application module
  var loginApp = angular.module('login', []);

  loginApp.controller('LoginController', [
    '$http',
    '$scope',
    '$window',
    function ($http, $scope, $window) {

      $scope.showLoginError = false;

      /**
       * Logins the user.
       * @see submitLoginForm in loyalty/assets/js/views/baseView.js
       */
      $scope.login = function () {
        var data = {
          'email': $scope.email,
          'password': $scope.password
        };

        var url = '/api/v2/auth/login/';
        $http.post(url, data)
          .success(function (response) {
            $window.location.href = '/directory/';
          })
          .error(function (response) {
            $scope.showLoginError = true;
            $scope.loginError = response.message;
          });
      };
    }]);

})();
