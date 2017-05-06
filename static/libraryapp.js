var app = angular.module("app", []);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.headers.common['X-CSRFToken'] = CSRF;
}]);

app.controller("books_ctrl", function($scope, $http, $timeout) {

	$scope.initialize = function() {

		$scope.editor = {"stock":true, "property":false};
		$http.get("/books").then($scope.update_view);
		$scope.toggled = false;
		$scope.mod_disabled = true;
		
		//for (book in $scope.books) {
		//	$scope.book["edit_mode"] = true;
		//}
	};

	$scope.update_view = function(response) {
		// Update all relevant Angular models

		// Populate table from Django database query
		$scope.books = angular.fromJson(response.data.books);
		// Fill in errors if any 
		$scope.errors = angular.fromJson(response.data.errors);;
	}

	$scope.add_book = function() {
		$http.post("/add", $scope.book).then($scope.update_view);
	};

	$scope.delete_book = function() {
		var delete_id = $scope.selected_row.children[0].children[0].innerHTML
		$http.post("/delete", {isbn:delete_id}).then($scope.update_view);
		$scope.selected_row = undefined;
	};
	
	$scope.edit_book = function() {
		$scope.editor["stock"] = !$scope.editor.stock;
		$scope.editor.property = true;
		$scope.selected_row = undefined;
	};

	$scope.select = function(event) {
		//console.log("select");
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

