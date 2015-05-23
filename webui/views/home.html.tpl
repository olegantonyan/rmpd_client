% include('_layout_header.html.tpl', page_home=True)

<h2 class="content-subhead">Home page</h2>

<form class="pure-form pure-form-aligned" action="/reboot" method="post">
    <fieldset>
        <legend>Reboot device</legend>
        <div class="pure-controls">
            <button type="submit" class="pure-button pure-button-primary">Reboot</button>
        </div>
    </fieldset>
</form>

% include('_layout_footer.html.tpl')