Title: Track My Money
Logo: {static images/logo.png}
Project_Start: 2012/07
Project_Authors: Alexandre Fonseca
Project_Version: 1.1.2
Project_Status: In development
Gallery:
    {static "images/2013-03-04 20.38.22.png"}||User selection
    {static "images/Screenshot_2013-03-02-02-45-39.png"}||Money node selection
    {static "images/Screenshot_2013-03-02-02-46-01.png"}||Money node edition
    {static "images/Screenshot_2013-03-02-02-46-17.png"}||Transaction list
    {static "images/Screenshot_2013-03-02-02-46-33.png"}||Transaction stats
    {static "images/Screenshot_2013-03-02-02-46-58.png"}||Category list
    {static "images/2013-03-04 20.49.22.png"}||Preferences


Track My Money is a simple revenue/expense tracker application for Android. It is built from the ground up with flexibility and security in mind, providing management of data from multiple users using encrypted SQLite databases. It is currently in development and supports Android versions as early as Gingerbread.<!--break-->

Current features:

* Support for multiple users.
* Encrypted databases.
* Support for multiple money nodes (places where money can flow to/from like banks, wallets, other people (e.g for loans)).
* Creation of transfers between money nodes.
* Support for custom categories per user.
* Management of immediate transactions (unique occurred transactions).
* Statistical data analysis with graphical representation.
* Import/Export from CSV files.
* Mathematical expression input for transaction values.

Planned features:

* Extended statistical analysis with bar/line charts.
* Management of scheduled transactions.
* Browsing transactions by category on all money nodes.
* Import/Export to various formats.

You can follow development on my Github repository: https://github.com/AlexJF/TrackMyMoney.

Summarized changelog: https://github.com/AlexJF/TrackMyMoney/blob/master/CHANGES

If you find this application useful, consider donating to help its development!

<form action="https://www.paypal.com/cgi-bin/webscr" method="post">
<p style="text-align: center"><a href="https://play.google.com/store/apps/details?id=net.alexjf.tmm"><img alt="Get it on Google Play" src="https://developer.android.com/images/brand/en_generic_rgb_wo_45.png"> &nbsp;&nbsp; </a><input name="cmd" value="_s-xclick" type="hidden"> <input name="encrypted" value="-----BEGIN PKCS7-----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-----END PKCS7-----
" type="hidden"> <input alt="PayPal - The safer, easier way to pay online!" name="submit" src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif" type="image" border="0"> <img alt="" src="https://www.paypalobjects.com/en_US/i/scr/pixel.gif" height="1" width="1" border="0"></p>
</form>
