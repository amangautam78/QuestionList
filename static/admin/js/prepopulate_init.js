'use strict';
{
    const $ = django.jQuery;
    const fields = $('#django-admin-prepopulated-fields-constants').data('prepopulatedFields');
    $.each(fields, function(index, field) {
<<<<<<< HEAD
        $(
            '.empty-form .form-row .field-' + field.name +
            ', .empty-form.form-row .field-' + field.name +
            ', .empty-form .form-row.field-' + field.name
        ).addClass('prepopulated_field');
=======
        $('.empty-form .form-row .field-' + field.name + ', .empty-form.form-row .field-' + field.name).addClass('prepopulated_field');
>>>>>>> 3b568933b8ffaa9fd7f40506bf945986e5a961ea
        $(field.id).data('dependency_list', field.dependency_list).prepopulate(
            field.dependency_ids, field.maxLength, field.allowUnicode
        );
    });
}
