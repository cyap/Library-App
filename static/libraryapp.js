var app = angular.module("app", []);

/* Generate table */
app.controller("booksCtrl", function($scope, $http) {

	$scope.update_books = function() {
		$http.get("/books").then(function(response) {
			$scope.books = response.data.books;	
		});
	};

	$scope.add_book = function() {
		/* Add function */
		$http.post("/add", {new_book: "insert_data_here"}).then(function(response) {
			$scope.books = response.data.books;
		});
		$scope.update_books()
	};

	$scope.update_books();
}) 