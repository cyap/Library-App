var app = angular.module("app", []);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.headers.common['X-CSRFToken'] = CSRF;
}]);

app.controller("books_ctrl", function($scope, $http, $timeout) {

	$scope.initialize = function() {

		$scope.editor = {}
		$http.get("/books").then($scope.update_view);
		$scope.toggled = false;
		$scope.mod_disabled = true;
	};

	$scope.update_view = function(response) {
		// Update all relevant Angular models
		$scope.editor = {}
		// Populate table from Django database query
		$scope.books = angular.fromJson(response.data.books);
		console.log($scope.books);
		// Fill in errors if any 
		$scope.errors = angular.fromJson(response.data.errors);;
	}

	$scope.add_book = function() {
		$http.post("/add", $scope.book).then($scope.update_view);
	};

	$scope.delete_book = function() {
		var delete_id = $scope.selected_row.children[1].children[0].innerHTML
		$http.post("/delete", {isbn:delete_id}).then($scope.update_view);
		$scope.selected_row = undefined;
	};
	
	$scope.edit_book = function() {
		// Map attribute (only stock editable in this case) to row and set visibility to true   
		$scope.editor["stock"+($scope.selected_row.children[0].innerHTML-1)] = true;
	};

	$scope.edit_update = function(new_stock, book) {
		$http.post("/edit", {stock:new_stock, isbn:book.fields.isbn}).then($scope.update_view);

	}


	$scope.select = function(event) {
		$scope.selected_row = event.target;
		angular.element($scope.selected_row).addClass("active");
		// Enable edit / delete buttons only when row is selected
		$scope.mod_disabled = !$scope.mod_disabled;
		angular.element(document.querySelectorAll(".mod-button")).removeClass("disabled");
	}

	$scope.blur = function(event) {
		// Style button disable - reversed if another row is selected
		angular.element(document.querySelectorAll(".mod-button")).addClass("disabled");

		// Preserve old row such that styling can occur after delay
		var old_row = $scope.selected_row;
		//console.log("blur");
		$timeout(function () {
			//console.log("onblur");
			// Actually disable button - delayed so onclick can work
			$scope.mod_disabled = !$scope.mod_disabled;
			angular.element(old_row).removeClass("active");
			//$scope.selected_row = undefined;
		}, 100)
		
	}

	$scope.toggle_add = function(event) {
		// Open / close submission form
		$scope.toggled = !$scope.toggled;
	}

	$scope.initialize();
})

