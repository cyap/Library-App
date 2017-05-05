var app = angular.module("app", []);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.headers.common['X-CSRFToken'] = CSRF;
}]);

app.controller("booksCtrl", function($scope, $http) {

	$scope.update_books = function() {
		// Populate table from Django database query
		$http.get("/books").then(function(response) {
			$scope.books = response.data.books;	
		});
	};

	$scope.add_book = function() {
		$http.post("/add", $scope.book).then(function(response) {
			$scope.books = angular.fromJson(response.data.books);
		});
	};

	// Populate table initially
	$scope.update_books();
}) 