/*
Copyright 2017 Ziadin Givan

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

https://github.com/givanz/VvvebJs
*/

gFlow.ComponentsGroup['Server Components'] = ["components/products", "components/product", "components/categories", "components/manufacturers", "components/search", "components/user", "components/product_gallery", "components/cart", "components/checkout", "components/filters", "components/product", "components/slider"];


gFlow.Components.add("components/product", {
    name: "Product",
    attributes: ["data-component-product"],

    image: "/static/gflow/libs/builder/icons/map.svg",
    html: '<iframe frameborder="0" src="https://maps.google.com/maps?&z=1&t=q&output=embed"></iframe>',
    
	properties: [
	{
        name: "Id",
        key: "id",
        htmlAttr: "id",
        inputtype: TextInput
    },
	{
        name: "Select",
        key: "id",
        htmlAttr: "id",
        inputtype: SelectInput,
        data:{
			options: [{
                value: "",
                text: "None"
            }, {
                value: "pull-left",
                text: "Left"
            }, {
                value: "pull-right",
                text: "Right"
            }]
       },
    },
	{
        name: "Select 2",
        key: "id",
        htmlAttr: "id",
        inputtype: SelectInput,
        data:{
			options: [{
                value: "",
                text: "nimic"
            }, {
                value: "pull-left",
                text: "gigi"
            }, {
                value: "pull-right",
                text: "vasile"
            }, {
                value: "pull-right",
                text: "sad34"
            }]
       },
    }]
});    


gFlow.Components.add("components/products", {
    name: "Products",
    attributes: ["data-component-products"],

    image: "/static/gflow/libs/builder/icons/products.svg",
    html: '<div class="form-group"><label>Your response:</label><textarea class="form-control"></textarea></div>',

    init: function (node)
	{
		$('.form-group[data-group]').hide();
		if (node.dataset.type != undefined)
		{
			$('.form-group[data-group="'+ node.dataset.type + '"]').show();
		} else
		{		
			$('.form-group[data-group]:first').show();
		}
	},
    properties: [{
        name: false,
        key: "type",
        inputtype: RadioButtonInput,
		htmlAttr:"data-type",
        data: {
            inline: true,
            extraclass:"btn-group-fullwidth",
            options: [{
                value: "autocomplete",
                text: "Autocomplete",
                title: "Autocomplete",
                icon:"la la-search",
                checked:true,
            }, {
                value: "automatic",
                icon:"la la-cog",
                text: "Configuration",
                title: "Configuration",
            }],
        },
		onChange : function(element, value, input) {
			
			$('.form-group[data-group]').hide();
			$('.form-group[data-group="'+ input.value + '"]').show();

			return element;
		}, 
		init: function(node) {
			return node.dataset.type;
		},            
    },{
        name: "Products",
        key: "products",
        group:"autocomplete",
        htmlAttr:"data-products",
        inline:true,
        col:12,
        inputtype: AutocompleteList,
        data: {
            url: "/admin/?module=editor&action=productsAutocomplete",
        },
    },{
        name: "Number of products",
        group:"automatic",
        key: "limit",
		htmlAttr:"data-limit",
        inputtype: NumberInput,
        data: {
            value: "8",//default
            min: "1",
            max: "1024",
            step: "1"
        },        
        getFromNode: function(node) {
            return 10
        },
    },{
        name: "Start from page",
        group:"automatic",
        key: "page",
		htmlAttr:"data-page",
        data: {
            value: "1",//default
            min: "1",
            max: "1024",
            step: "1"
        },        
        inputtype: NumberInput,
        getFromNode: function(node) {
            return 0
        },
    },{
        name: "Order by",
        group:"automatic",
        key: "order",
		htmlAttr:"data-order",
        inputtype: SelectInput,
        data: {
            options: [{
				value: "price_asc",
                text: "Price Ascending"
            }, {
                value: "price_desc",
                text: "Price Descending"
            }, {
                value: "date_asc",
                text: "Date Ascending"
            }, {
                value: "date_desc",
                text: "Date Descending"
            }, {
                value: "sales_asc",
                text: "Sales Ascending"
            }, {
                value: "sales_desc",
                text: "Sales Descending"
            }]
		}
	},{
        name: "Category",
        group:"automatic",
        key: "category",
		htmlAttr:"data-category",
        inline:true,
        col:12,
        inputtype: AutocompleteList,
        data: {
            url: "/admin/?module=editor&action=productsAutocomplete",
        },

	},{
        name: "Manufacturer",
        group:"automatic",
        key: "manufacturer",
		htmlAttr:"data-manufacturer",
        inline:true,
        col:12,
        inputtype: AutocompleteList,
        data: {
            url: "/admin/?module=editor&action=productsAutocomplete",
		}
	},{
        name: "Manufacturer 2",
        group:"automatic",
        key: "manufacturer 2",
		htmlAttr:"data-manufacturer2",
        inline:true,
        col:12,
        inputtype: AutocompleteList,
        data: {
            url: "/admin/?module=editor&action=productsAutocomplete",
        },
    }]
});

gFlow.Components.add("components/manufacturers", {
    name: "Manufacturers",
    classes: ["component_manufacturers"],
    image: "/static/gflow/libs/builder/icons/categories.svg",
    html: '<div class="form-group"><label>Your response:</label><textarea class="form-control"></textarea></div>',
    properties: [{
        nolabel:false,
        inputtype: TextInput,
        data: {text:"Fields"}
	},{
        name: "Name",
        key: "category",
        inputtype: TextInput
	},{
        name: "Image",
        key: "category",
        inputtype: TextInput
	}
    ]
});

gFlow.Components.add("components/categories", {
    name: "Categories",
    classes: ["component_categories"],
    image: "/static/gflow/libs/builder/icons/categories.svg",
    html: '<div class="form-group"><label>Your response:</label><textarea class="form-control"></textarea></div>',
    properties: [{
        name: "Name",
        key: "name",
        htmlAttr: "src",
        inputtype: FileUploadInput
    }]
});
gFlow.Components.add("components/search", {
    name: "Search",
    classes: ["component_search"],
    image: "/static/gflow/libs/builder/icons/search.svg",
    html: '<div class="form-group"><label>Your response:</label><textarea class="form-control"></textarea></div>',
    properties: [{
        name: "asdasdad",
        key: "src",
        htmlAttr: "src",
        inputtype: FileUploadInput
    }, {
        name: "34234234",
        key: "width",
        htmlAttr: "width",
        inputtype: TextInput
    }, {
        name: "d32d23",
        key: "height",
        htmlAttr: "height",
        inputtype: TextInput
    }]
});
gFlow.Components.add("components/user", {
    name: "User",
    classes: ["component_user"],
    image: "/static/gflow/libs/builder/icons/user.svg",
    html: '<div class="form-group"><label>Your response:</label><textarea class="form-control"></textarea></div>',
    properties: [{
        name: "asdasdad",
        key: "src",
        htmlAttr: "src",
        inputtype: FileUploadInput
    }, {
        name: "34234234",
        key: "width",
        htmlAttr: "width",
        inputtype: TextInput
    }, {
        name: "d32d23",
        key: "height",
        htmlAttr: "height",
        inputtype: TextInput
    }]
});
gFlow.Components.add("components/product_gallery", {
    name: "Product gallery",
    classes: ["component_product_gallery"],
    image: "/static/gflow/libs/builder/icons/product_gallery.svg",
    html: '<div class="form-group"><label>Your response:</label><textarea class="form-control"></textarea></div>',
    properties: [{
        name: "asdasdad",
        key: "src",
        htmlAttr: "src",
        inputtype: FileUploadInput
    }, {
        name: "34234234",
        key: "width",
        htmlAttr: "width",
        inputtype: TextInput
    }, {
        name: "d32d23",
        key: "height",
        htmlAttr: "height",
        inputtype: TextInput
    }]
});
gFlow.Components.add("components/cart", {
    name: "Cart",
    classes: ["component_cart"],
    image: "/static/gflow/libs/builder/icons/cart.svg",
    html: '<div class="form-group"><label>Your response:</label><textarea class="form-control"></textarea></div>',
    properties: [{
        name: "asdasdad",
        key: "src",
        htmlAttr: "src",
        inputtype: FileUploadInput
    }, {
        name: "34234234",
        key: "width",
        htmlAttr: "width",
        inputtype: TextInput
    }, {
        name: "d32d23",
        key: "height",
        htmlAttr: "height",
        inputtype: TextInput
    }]
});
gFlow.Components.add("components/checkout", {
    name: "Checkout",
    classes: ["component_checkout"],
    image: "/static/gflow/libs/builder/icons/checkout.svg",
    html: '<div class="form-group"><label>Your response:</label><textarea class="form-control"></textarea></div>',
    properties: [{
        name: "asdasdad",
        key: "src",
        htmlAttr: "src",
        inputtype: FileUploadInput
    }, {
        name: "34234234",
        key: "width",
        htmlAttr: "width",
        inputtype: TextInput
    }, {
        name: "d32d23",
        key: "height",
        htmlAttr: "height",
        inputtype: TextInput
    }]
});
gFlow.Components.add("components/filters", {
    name: "Filters",
    classes: ["component_filters"],
    image: "/static/gflow/libs/builder/icons/filters.svg",
    html: '<div class="form-group"><label>Your response:</label><textarea class="form-control"></textarea></div>',
    properties: [{
        name: "asdasdad",
        key: "src",
        htmlAttr: "src",
        inputtype: FileUploadInput
    }, {
        name: "34234234",
        key: "width",
        htmlAttr: "width",
        inputtype: TextInput
    }, {
        name: "d32d23",
        key: "height",
        htmlAttr: "height",
        inputtype: TextInput
    }]
});
gFlow.Components.add("components/product", {
    name: "Product",
    classes: ["component_product"],
    image: "/static/gflow/libs/builder/icons/product.svg",
    html: '<div class="form-group"><label>Your response:</label><textarea class="form-control"></textarea></div>',
    properties: [{
        name: "asdasdad",
        key: "src",
        htmlAttr: "src",
        inputtype: FileUploadInput
    }, {
        name: "34234234",
        key: "width",
        htmlAttr: "width",
        inputtype: TextInput
    }, {
        name: "d32d23",
        key: "height",
        htmlAttr: "height",
        inputtype: TextInput
    }]
});
gFlow.Components.add("components/slider", {
    name: "Slider",
    classes: ["component_slider"],
    image: "/static/gflow/libs/builder/icons/slider.svg",
    html: '<div class="form-group"><label>Your response:</label><textarea class="form-control"></textarea></div>',
    properties: [{
        name: "asdasdad",
        key: "src",
        htmlAttr: "src",
        inputtype: FileUploadInput
    }, {
        name: "34234234",
        key: "width",
        htmlAttr: "width",
        inputtype: TextInput
    }, {
        name: "d32d23",
        key: "height",
        htmlAttr: "height",
        inputtype: TextInput
    }]
});
