<h1>Visitors</h1>
<ul>
%for (n,ip) in visits:
    <li>{{ip}} - {{n}}</li>
%end 
</ul>