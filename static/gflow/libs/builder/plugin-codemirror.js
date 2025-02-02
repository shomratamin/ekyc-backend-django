gFlow.CodeEditor = {
	
	isActive: false,
	oldValue: '',
	doc:false,
	codemirror:false,
	codemirror2:false,
	
	init: function(doc) {

		if (this.codemirror == false)		
		{
			this.codemirror = CodeMirror.fromTextArea(document.querySelector("#gflow-code-editor textarea"), {
				mode: 'text/html',
				lineNumbers: true,
				autofocus: true,
				lineWrapping: true,
				//viewportMargin:Infinity,
				theme: 'the-matrix',
				autoCloseTags: true
			});
		
			// this.codemirror2 = CodeMirror.fromTextArea(document.querySelector("#gflow-code-editor textarea"), {
			// 	mode: 'jinja2',
			// 	lineNumbers: true,
			// 	autofocus: true,
			// 	lineWrapping: true,
			// 	//viewportMargin:Infinity,
			// 	theme: 'ayu-dark'
			// });
			
			this.isActive = true;
			this.codemirror.getDoc().on("change", function (e, v) { 
				if (v.origin != "setValue")
				delay(gFlow.Builder.setHtml(e.getValue()), 1000);
			});

			CodeMirror.commands["selectAll"](this.codemirror)

			function get_selected_code () {
				return { from: this.codemirror.getCursor(true), to: this.codemirror.getCursor(false)}
			}

			this.format_selection = function() {
				let code_range = get_selected_code()
				this.codemirror.autoFormatRange(code_range.from, code_range.to)
			}

			function comment_selection () {
				let code_range = get_selected_code()
				this.codemirror.comentRange(code_range.from, code_range.to)
			}

			this.codemirror
		}
		
		
		//_self = this;
		gFlow.Builder.frameBody.on("gflow.undo.add gflow.undo.restore", function (e) { gFlow.CodeEditor.setValue(e);});
		//load code when a new url is loaded
		gFlow.Builder.documentFrame.on("load", function (e) { gFlow.CodeEditor.setValue();});

		this.isActive = true;
		this.setValue();

		// return this.codemirror;
	},

	setValue: function(value) {
		if (this.isActive == true)
		{
			var scrollInfo = this.codemirror.getScrollInfo();
			this.codemirror.setValue(gFlow.Builder.getHtml());
			this.codemirror.scrollTo(scrollInfo.left, scrollInfo.top);
		}
	},

	destroy: function(element) {
		/*
		//save memory by destroying but lose scroll on editor toggle
		this.codemirror.toTextArea();
		this.codemirror = false;
		*/ 
		this.isActive = false;
	},

	toggle: function() {
		if (this.isActive != true)
		{
			this.isActive = true;
			return this.init();
		}
		this.isActive = false;
		this.destroy();
	}
}
