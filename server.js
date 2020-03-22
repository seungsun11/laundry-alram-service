var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var session = require('express-session');
var fs = require('fs');
var cors = require('cors');

app.use(cors());

// var corsOptions = {
//     origin: 'http://192.168.122.124',
//     optionsSuccessStatus: 200,
//     credentials:true,
//     'Access-Control-Allow-Credentials': true,
//     'Access-Control-Allow-Origin':true
// }

// app.use(cors(corsOptions));

// /* configure CORS issue */
// app.use((req, res, next) => {
//     const whiteList = [
//         'localhost',
//         'ssal.sparcs.org',
//         'http://192.168.122.124',
//         'http://143.248.36.102:3000'
//     ];
//     const origin = req.header['origin'];
//     whiteList.every(el => {
//         if (!origin) return false;
//         if (origin.indexOf(el) !== -1) {
//             res.set('Access-Control-Allow-Origin', origin);
//             return false;
//         }
//         return true;
//     });
//     res.set('Access-Control-Allow-Credentials', true);
//     res.set('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, x-timebase, Link');
//     res.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, PATCH, OPTIONS');
//     res.set('Access-Control-Expose-Headers', 'Link');
//     return next();
// });


//ejs 템플릿 엔진
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.engine('html', require('ejs').renderFile);

var server = app.listen(3000, function(){
    console.log("Express server has started on port 3000")
});

app.use(express.static('public'));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded());
// secret: 쿠키 임의 변조 방지, 원하는 값 넣기
// resave: 세션을 언제 저장할지 정하기
// saveUninitialized: 새로 생겼지만 변경되지 않은 세션 의미, true 권장
app.use(session({
    secret: '@#@$MYSIGN#@$#$',
    resave: false,
    saveUninitialized: true
}));

var router = require('./router/main')(app, fs);
// var router2 = require('/router/update')(app, fs);