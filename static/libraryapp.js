var app = angular.module("app", []);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.headers.common['X-CSRFToken'] = CSRF;
}]);

app.controller("books_ctrl", function($scope, $http, $timeout) {

	$scope.initialize = function() {
		$scope.editor = {}
		$http.get("/books").then($scope.update_view);
		$scope.add_open = false;
		$scope.tr_open = false;
	};

	$scope.update_view = function(response) {
		$scope.editor = {}
		// Populate table from Django database query
		$scope.books = angular.fromJson(response.data.books);
		// Fill in errors if any 
		$scope.errors = angular.fromJson(response.data.errors);;
	}

	$scope.add_book = function() {
		$http.post("/add", $scope.book).then($scope.update_view);
	};

	$scope.delete_book = function() {
		var delete_id = $scope.selected_row.children[1].children[0].innerHTML
		$http.post("/delete", {isbn:delete_id}).then($scope.update_view);
	};
	
	$scope.edit_book = function() {
		// Map attribute (only stock editable in this case) to row and set visibility to true   
		$scope.editor["stock"+($scope.selected_row.children[0].innerHTML-1)] = true;
	};

	$scope.edit_update = function(new_stock, book) {
		$http.post("/edit", {stock:new_stock, isbn:book.fields.isbn})
		.then($scope.update_view);
	}

	$scope.transaction = function() {
		$scope.tr.transaction_date = $scope.transaction_date_year + "-" 
			+ $scope.transaction_date_month + "-" + $scope.transaction_date_day;
		$scope.tr.other_date = $scope.other_date_year + "-" 
			+ $scope.other_date_month + "-" + $scope.other_date_day;
		$http.post("/transaction", {isbn:$scope.transaction_isbn, tr:$scope.tr})
		.then($scope.update_view);
		$scope.tr = {}
	}

	$scope.close_transaction = function (event) {
		var target_key = $scope.transactions[event.target.parentNode.parentNode.children[0].innerHTML-1].pk;
		$http.post("/close_transaction", {target_key:target_key}).then(function(response) {
			$scope.transactions = angular.fromJson(response.data.transactions);
			$scope.books = angular.fromJson(response.data.books);
		})
	}

	$scope.select = function(event) {
		$scope.tr_open = false;
		$scope.selected_row = event.target;
		angular.element($scope.selected_row).addClass("active");

		// Load transactions for selected row
		$http.post("/get_transactions", {target:$scope.selected_row.children[1].children[0].innerHTML})
			.then(function(response) {
				$scope.transactions = angular.fromJson(response.data.transactions);
			})
	}

	$scope.blur = function(event) {
		// Preserve old row such that styling can occur after delay
		var old_row = $scope.selected_row;

		$timeout(function () {
			// Disable button - delayed so onclick can work
			angular.element(old_row).removeClass("active");
			if (old_row == $scope.selected_row) {
				$scope.selected_row = undefined;
			}
		}, 150)
	}

	$scope.toggle_add = function() {
		// Open / close submission form
		$scope.add_open = !$scope.add_open;
		$scope.tr_open = false;
	}

	$scope.toggle_tr = function() {

		$scope.errors = {};
		// Manage panes
		$scope.tr_open = !$scope.tr_open;
		$scope.add_open = false;

		$scope.tr = {};
		$scope.transaction_isbn = $scope.selected_row.children[1].children[0].innerHTML
	}

	$scope.initialize();
})

