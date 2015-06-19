function Url(){
    var self = this;
    self.longUrl = ko.observable("");
    self.shortUrl = ko.observable("");
    self.resultUrl = ko.observable("");
    self.save = function() {
            
            $.ajax({
            url: "http://127.0.0.1:5000/", 
            type:"post",
            data: ko.toJSON(self),
            contentType:"application/json",
            success: function(data){
                console.log(data);
                self.resultUrl(data.url);
            }

        });
  
    };

}

ko.applyBindings(new Url());