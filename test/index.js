var bhttp = require('bhttp')
var request = require('request')

exports.handler = (event, context, callback) => {
	//code grant
	var code = event.code;
	console.log(code);
	//request header content type
	const options = {
		headers: {
		  'Content-Type': 'application/x-www-form-urlencoded',
		},
	};
	//get amazone login access token
	bhttp.post('https://api.amazon.com/auth/o2/token', 'grant_type=authorization_code&code='+code+'&client_id=amzn1.application-oa2-client.209802e6f10e432f9dde9982bd375249&client_secret=f6dad1825cadf297222922c8104fc2f4829e4412758dc41cf177c9f7a6c3f2d7', options).then(response => {
		const body = response.body;
		console.log(body);
		//token variable
		var token = body.access_token;
		console.log(token);
		//get amazon user info
		request('https://api.amazon.com/user/profile?access_token=' + token, function (error, response, body) {
			console.log(body);
			//lambda callback
			callback(null, body);
	})
	});
};
