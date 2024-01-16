document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#send').addEventListener('click', () => send_mail());

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  document.querySelector('#compose-header').textContent = 'New Email'
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  document.querySelector('#compose-subject').disabled = false
  document.querySelector('#compose-recipients').disabled = false
}

function load_mailbox(mailbox) {
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        emails.forEach(email => {
            const emailDiv = document.createElement('div');
            emailDiv.classList.add('eachmail');
            emailDiv.style.border = '2px solid black';
            emailDiv.innerHTML = `
              <div>
                <span style='font-weight: 700; margin-right: 15px'>${email.sender}</span>
                <span style='font-weight: 500'>${email.subject}</span>
              </div>
              <span style='color: black'>${email.timestamp}</span>
            `;
            if (email.read == true){
              emailDiv.style.background = 'gray'
            }
            else{
              emailDiv.style.bacground = 'white'
            }
            emailDiv.style.color = 'black';
            emailDiv.style.padding = '10px';
            emailDiv.style.display = 'flex';
            emailDiv.style.flexDirection = 'row';
            emailDiv.style.justifyContent = 'space-between';
            emailDiv.style.marginBottom = '10px'
            document.querySelector('#emails-view').appendChild(emailDiv);
            emailDiv.addEventListener('click', () => get_email(email.id));
        });
    });

}

function send_mail(){
  let recipients = document.querySelector('#compose-recipients').value;
  let subject = document.querySelector('#compose-subject').value;
  let body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      confirm(result.message)
      load_mailbox('sent')
  });
}
function get_email(id){
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    if (email.read == false){
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
    }
    document.querySelector('#email-view').innerHTML = `
      <div class='topmail'>
        <div id='archive-button'></div>
        <div class='topline'>
          <label>From: </label>
          <span>${email.sender}</span>
        </div>
        <div class='topline'>
          <label>To: </label>
          <span>${email.recipients}</span>
        </div>
        <div class='topline'>
          <label>Subject: </label>
          <span>${email.subject}</span>
        </div>
        <div class='topline'>
          <label>Timestamp: </label>
          <span>${email.timestamp}</span>
        </div>
        <button class="btn btn-primary" onclick='reply(${email.id})' id='reply-button' >Reply</button>
      </div>
      <hr>
      <div >
        ${email.body}
      </div>`;
      const archiveButton = document.createElement('button');
            archiveButton.classList.add('btn', 'btn-primary');
      let user = document.querySelector('#user-auth').textContent;
      if(email.sender == user){
        archiveButton.style.display= 'none'
      }
      if(email.archived == false){
            archiveButton.addEventListener('click', () => archive(email.id));
            archiveButton.textContent = 'Archive';
      }
      else{
        archiveButton.addEventListener('click', () => unarchive(email.id));
        archiveButton.textContent = 'Un-archive'  ;  
  
      }
      let archivebutton =  document.querySelector('#archive-button')
      archivebutton.append(archiveButton)
  });
}
function archive(id){
  fetch(`/emails/${id}`,{
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  })
  confirm('Archived Successfully')
  load_mailbox('inbox')
}
function unarchive(id){
  fetch(`/emails/${id}`,{
    method: 'PUT',
    body: JSON.stringify({
        archived: false
    })
  })
  confirm('Unarchived Successfully')
  load_mailbox('inbox')
}
function reply(id){
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
  document.querySelector('#compose-recipients').value = `${email.sender}`;
  document.querySelector('#compose-recipients').disabled = true
  if(email.subject.startsWith('Re:')){
    document.querySelector('#compose-subject').value = `${email.subject}`;
  }
  else{
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
  }
  document.querySelector('#compose-subject').disabled = true
  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
  document.querySelector('#compose-header').textContent = 'Reply Email'
  })
}
