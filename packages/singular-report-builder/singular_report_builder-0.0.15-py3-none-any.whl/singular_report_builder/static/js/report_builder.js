async function printReport(ajax_url, queryset, kwargs = {}) {
    kwargs = JSON.stringify(kwargs)
    queryset = JSON.stringify(queryset)
    const form = $(`<form method="post" action="${ajax_url}" target="_blank">
                    <input type="hidden" name="queryset" value='${queryset}'>
                    <input type="hidden" name="kwargs" value='${kwargs}'>
                    <input type="hidden" name="csrfmiddlewaretoken" value="${csfr_token_js}">
                </form>`)
    $('body').append(form)
    form.submit()
    form.remove()
    $('.ms-preload').addClass('hidden')
}