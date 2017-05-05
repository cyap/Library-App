var app = angular.module("app", []);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.headers.common['X-CSRFToken'] = CSRF;
}]);

app.controller("books_ctrl", function($scope, $http) {

	$scope.update_view = function(response) {
		// Update all relevant Angular models

		// Populate table from Django database query
		$scope.books = angular.fromJson(response.data.books);

		// Fill in errors if any 
		var errors = angular.fromJson(response.data.errors);
		for (error in errors) {
			$scope[error] = errors[error];
		}
	}

	$scope.initialize = function() {
		$http.get("/books").then($scope.update_view);
	};

	$scope.add_book = function() {
		$http.post("/add", $scope.book).then($scope.update_view);
	};

	$scope.delete_book = function() {
		$http.post("/delete", $scope.book).then($scope.update_view);
	};

	$scope.edit_book = function() {
		$http.post("/edit", $scope.book).then($scope.update_view);
	};

	// Initial table population
	$scope.initialize();
}) 