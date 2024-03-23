function signup() {
  Swal.fire({
    html: `
      <div class="main-container" style="width: 100%;">
        <h1 class="title-text">SIGN UP</h1>
        <h6 class="subtitle-text">FILL IN THE FIELDS BELOW</h6>
        <div class="transparent-container">
          <input id="swal-input-name" class="swal2-input" placeholder="NAME">
          <input id="swal-input-email" class="swal2-input" placeholder="EMAIL">
        </div>
      </div>
    `,
    focusConfirm: false,
    showCancelButton: true,
    allowOutsideClick: false,
    allowEscapeKey: false,
    allowEnterKey: false,
    showLoaderOnConfirm: true,
    confirmButtonText: 'SIGN UP',
    cancelButtonText: 'CANCEL',
    preConfirm: async () => {
      const name = document.getElementById('swal-input-name').value;
      const email = document.getElementById('swal-input-email').value;

      if (!name || !email) {
        Swal.showValidationMessage('<h6 class="subtitle-text">FILL IN ALL FIELDS</h6>');
      }
      
      try {
        response = await axios.post('/signup', { name, email });

        const { data } = response;

        Swal.fire({
          icon: 'success',
          html: `
            <div class="main-container" style="width: 100%;">
              <h1 class="title-text">SUCCESS</h1>
              <h6 class="subtitle-text">
                YOU HAVE SUCCESSFULLY SIGNED UP!
                </br>WELCOME, ${data.name}!
              </h6>
              <div class="transparent-container">
                <img src="${data.image}" class="image-capture">
              </div>
            </div>
          `,
          confirmButtonText: "CLOSE"
        });
      } catch (error) {
        const { response } = error;

        const message = response?.data?.message || 'SOMETHING WENT WRONG';

        Swal.showValidationMessage(`<h6 class="subtitle-text">${message}</h6>`);
      }
      
      return false;
    }
  })
}

function signin() {
  Swal.fire({
    html: `
      <div class="main-container" style="width: 100%;">
        <h1 class="title-text">SIGN IN</h1>
        <h6 class="subtitle-text">FILL IN THE FIELDS BELOW</h6>
        <div class="transparent-container">
          <input id="swal-input-email" class="swal2-input" placeholder="EMAIL">
        </div>
      </div>
    `,
    focusConfirm: false,
    showCancelButton: true,
    allowOutsideClick: false,
    allowEscapeKey: false,
    allowEnterKey: false,
    showLoaderOnConfirm: true,
    confirmButtonText: 'SIGN IN',
    cancelButtonText: 'CANCEL',
    preConfirm: async () => {
      const email = document.getElementById('swal-input-email').value;

      if (!email) {
        Swal.showValidationMessage('<h6 class="subtitle-text">FILL IN ALL FIELDS</h6>');
      }
      
      try {
        response = await axios.post('/signin', { email });

        const { data } = response;

        Swal.fire({
          icon: 'success',
          html: `
            <div class="main-container" style="width: 100%;">
              <h1 class="title-text">SUCCESS</h1>
              <h6 class="subtitle-text">WELCOME BACK, ${data.name}!</h6>
              <div class="transparent-container">
                <img src="${data.image}" class="image-capture">
              </div>
            </div>
          `,
          confirmButtonText: "CLOSE"
        });
      } catch (error) {
        const { response } = error;

        const message = response?.data?.message || 'SOMETHING WENT WRONG';

        Swal.showValidationMessage(`<h6 class="subtitle-text">${message}</h6>`);
      }

      return false;
    }
  })
}

function capture() {
  Swal.fire({
    html: `
      <div class="main-container" style="width: 100%;">
        <h1 class="title-text">CAPTURE</h1>
        <h6 class="subtitle-text">TAKE A PHOTO</h6>
        <div id="capture-container" class="transparent-container">
          <h6 class="subtitle-text">CLICK THE BUTTON BELOW TO TAKE A PHOTO...</h6>
        </div>
      </div>
    `,
    focusConfirm: false,
    showCancelButton: true,
    allowOutsideClick: false,
    allowEscapeKey: false,
    allowEnterKey: false,
    showLoaderOnConfirm: true,
    confirmButtonText: 'CAPTURE',
    cancelButtonText: 'CANCEL',
    preConfirm: async () => {
      try {
        const response = await axios.post('/capture');
        const { data } = response;

        const image = data.image;

        document.getElementById('capture-container').innerHTML = `
          <img src="${image}" class="image-capture">
        `;
      } catch (error) {
        const { response } = error;

        const message = response?.data?.message || 'SOMETHING WENT WRONG';

        Swal.showValidationMessage(`<h6 class="subtitle-text">${message}</h6>`);
      }

      return false;
    }
  })
}

function quit() {
  window.close();
}