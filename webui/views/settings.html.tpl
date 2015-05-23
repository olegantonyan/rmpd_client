% include('_layout_header.html.tpl', page_settings=True)

<h2 class="content-subhead">Settings</h2>
                        
<form class="pure-form pure-form-aligned" action="/settings/change_address" method="post">
    <fieldset>
        <legend>Main IP address</legend>
        <div class="pure-controls">
            <label for="use_dhcp" class="pure-checkbox">
                % dhcp_state_checkbox = 'checked' 
                % static_ip_control_mode = 'none'
                % if addr_form_values['dhcp'] != True:
                % dhcp_state_checkbox = '' 
                % static_ip_control_mode = 'block'
                %end
                <input id="use_dhcp" name="use_dhcp" type="checkbox" {{dhcp_state_checkbox}} onclick="toggle_div('static_ip_controls', !this.checked);"> DHCP         
                <script> function toggle_div(id, show) { document.getElementById(id).style.display = show ? 'block' : 'none'; } </script>
            </label>
        </div>
        <div id="static_ip_controls" style="display:{{static_ip_control_mode}};">
            <div class="pure-control-group">
                <label for="addr">Address</label>
                <input id="addr" name="addr" type="text" placeholder="Static IPv4 address (i.e. 192.168.1.25)" class="pure-input-2-3" value="{{addr_form_values['addr']}}">
            </div>
        
            <div class="pure-control-group">
                <label for="netmask">Netmask</label>
                <input id="netmask" name="netmask" type="text" placeholder="Static IPv4 netmask (i.e. 255.255.255.0)" class="pure-input-2-3" value="{{addr_form_values['netmask']}}">
            </div>
            
            <div class="pure-control-group">
                <label for="gateway">Gateway</label>
                <input id="gateway" name="gateway" type="text" placeholder="Static IPv4 gateway (i.e. 192.168.1.1)" class="pure-input-2-3" value="{{addr_form_values['gateway']}}">
            </div>
            
            <div class="pure-control-group">
                <label for="nameservers">Nameserver(s)</label>
                <input id="nameservers" name="nameservers" type="text" placeholder="Static IPv4 DNS (i.e. 192.168.1.1, 8.8.8.8)" class="pure-input-2-3" value="{{addr_form_values['nameservers']}}">
            </div>
        </div>
        <div class="pure-controls">
            <button type="submit" class="pure-button pure-button-primary">Submit</button>
        </div>
    </fieldset>
</form>

<form class="pure-form pure-form-aligned" action="/settings/change_password" method="post">
    <fieldset>
        <legend>Change admin password</legend>
        <div class="pure-control-group">
            <label for="current_password">Current password</label>
            <input type="password" placeholder="Current password" name="current_password" class="pure-input-2-3">
        </div>
        <div class="pure-control-group">
            <label for="new_password">New password</label>
            <input type="password" placeholder="New password" name="new_password" class="pure-input-2-3">
        </div>
        <div class="pure-controls">
            <button type="submit" class="pure-button pure-button-primary">Submit</button>
        </div>
    </fieldset>
</form>

% include('_layout_footer.html.tpl')