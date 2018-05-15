

class viewMapButton extends React.Component {
	viewMap(){
		let parkList = [];
		fetch('/locate_park.json')
		.then((response) => response.json()).then(function(data) {
			let mapattr = JSON.parse(data);
			let mapCoordinates = {};
			let coordinates = mapattr.coordinates;
			let length = coordinates.length;
			for (let i =0; i<1; i++) {
				mapCoordinates = {
					position: {
						lat: parseFloat(mapattr.coordinates[i].lat),
						lng : parseFloat(mapattr.coordinates[i].lng)						
					},
					title : mapattr.coordinates[i].name,
				};
			parkList.push(mapCoordinates);
			}
			parkList.forEach(function(element) {
				let marker = new google.maps.Marker ({
					position : element.position,
					title : element.name,
					map: map
				});
			});
		});
	}
}
		
