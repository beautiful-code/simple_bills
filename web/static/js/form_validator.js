var CustomFormValidator = function(config) {
  var self = this;
  self.submitBtnLoadingText = config.submitBtnLoadingText || 'Adding ...';
  self.requiredFields = config.requiredFields || [];
  self.requiredFieldsInputs = [];

  for(var i = 0; i < self.requiredFields.length; i++) {
    var $inputEle = $("[ng-model='" + self.requiredFields[i] + "'");
    self.requiredFieldsInputs.push($inputEle);
  }

  self.validateFields = function() {
    for(var i = 0; i < self.requiredFieldsInputs.length; i++) {
      if(!self.requiredFieldsInputs[i].val()) {
        return false;
      }
    }

    return true;
  };

  self.highlightRequiredFields = function() {
    for(var i = 0; i < self.requiredFieldsInputs.length; i++) {
      var $inputEle = self.requiredFieldsInputs[i];

      if(!$inputEle.val()) {
        $inputEle.addClass('invalid');
      } else {
        $inputEle.removeClass('invalid');
      }
    }
  };

  self.submitForm = function($event) {
    if(self.validateFields()) {
      var $submitBtn = $($event.currentTarget);
      $submitBtn.addClass('disabled');
      $submitBtn.html(self.submitBtnLoadingText);
      $submitBtn.closest('form').submit();
    } else {
      self.highlightRequiredFields();
    }
  };
};
