document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function view_email(id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  fetch('/emails/' + id)
    .then(response => response.json())
    .then(email => {
      // Print email
      console.log(email);

      fetch('/emails/' + id, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })
      if (!email.archived) {
        document.querySelector('#email-view').innerHTML += `
        <div class="email-contaner">
        <p><strong>Sender</strong>: ${email.sender} </p>
        <p><strong>Recipient</strong>: ${email.recipient} </p>
        <p><strong>Timestamp</strong>: ${email.timestamp} </p>
        <p><strong>Subject</strong>: ${email.subject} </p>

        <br><br>

        <p><strong>Body</strong>:<br> ${email.body} </p>

        <br><br>

        <button class='btn btn-outline-primary' onclick="reply_email(${email.id})">Reply</p>
        <button class='btn btn-outline-primary' onclick="archive_email(${email.id})">Archive</p>
        </div>
      `
      } else {

        document.querySelector('#email-view').innerHTML += `
        <div class="email-contaner">
        <p><strong>Sender</strong>: ${email.sender} </p>
        <p><strong>Recipient</strong>: ${email.recipient} </p>
        <p><strong>Timestamp</strong>: ${email.timestamp} </p>
        <p><strong>Subject</strong>: ${email.subject} </p>

        <br><br>

        <p><strong>Body</strong>:<br> ${email.body} </p>

        <br><br>

        <button class='btn btn-outline-primary' onclick="reply_email(${email.id})">Reply</p>
        <button class='btn btn-outline-primary' onclick="unarchive_email(${email.id})">Unarchive</p>
        </div>
        
        `
      }

    });

}

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  const composeForm = document.querySelector('#compose-form');
  composeForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const compose_recipients = document.querySelector('#compose-recipients').value;
    const compose_suject = document.querySelector('#compose-subject').value;
    const compose_body = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: compose_recipients,
        subject: compose_suject,
        body: compose_body
      })
    })
      .then(response => response.json())
      .then(result => {
        console.log(result);
      });

    return load_mailbox('sent');

  })
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch('/emails/' + mailbox)
    .then(response => response.json())
    .then(emails => {
      // Print emails
      console.log(emails);
      document.querySelector('#emails-view').innerHtml += `<div id="mail-container"></div>`
      emails.forEach(email => {
        if (email.read) {
          document.querySelector('#emails-view').innerHTML += `
          <div onclick="view_email(${email.id})" class="card" style="background-color: silver;">
            <div class="card-body" style="display: flex; align-items: center; justify-content: space-between;">
              <p> ${email.sender} </p>
              <p> ${email.subject} </p>
              <p> ${email.timestamp} </p>
            </div>
          </div>
          `
        } else {
          document.querySelector('#emails-view').innerHTML += `
          <div onclick="view_email(${email.id})" class="card" style="background-color: white;">
            <div class="card-body" style="display: flex; align-items: center; justify-content: space-between;">
              <p> <strong>${email.sender}<strong> </p>
              <p> ${email.subject} </p>
              <p> ${email.timestamp} </p>
            </div>
          </div>
          `
        }
      })
    });
}

function archive_email(id) {
  fetch('/emails/' + id, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true
    })
  })
  load_mailbox('inbox');
}

function unarchive_email(id) {
  fetch('/emails/' + id, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  })
  load_mailbox('inbox');
}

function reply_email(id) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  fetch('/emails/' + id)
    .then(response => response.json())
    .then(email => {

      // fill out composition fields
      document.querySelector('#compose-recipients').value = email.sender;
      document.querySelector('#compose-subject').value = "Re:" + email.subject;
      document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote: \r\n ${email.body}`;

      const composeForm = document.getElementById('compose-form');
      composeForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const compose_recipients = document.querySelector('#compose-recipients').value;
        const compose_suject = document.querySelector('#compose-subject').value;
        const compose_body = document.querySelector('#compose-body').value;

        fetch('/emails', {
          method: 'POST',
          body: JSON.stringify({
            recipients: compose_recipients,
            subject: compose_suject,
            body: compose_body
          })
        })
          .then(response => response.json())
          .then(result => {
            console.log(result);
          });

        return load_mailbox('sent');

      })
    });
}


