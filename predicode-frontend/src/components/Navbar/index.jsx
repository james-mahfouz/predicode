const Navbar = () => {
  return (
    <div>
      <section className="navbar">
        <div className="logo">
          <img src={logo} />
        </div>
        {!signedIn && (
          <div className="signin_button">
            <Button
              label={!isSmallScreen && "Sign-In"}
              icon="pi pi-sign-in"
              className="btn"
              onClick={go_signin}
            />
          </div>
        )}
        {signedIn && (
          <div className="signin_button">
            <Button
              icon="pi pi-user"
              rounded
              outlined
              severity="info"
              aria-label="User"
              onClick={() => setVisibleRight(true)}
              style={{ borderWidth: "3px" }}
              className="bolder-icon"
            />
          </div>
        )}
      </section>

      <section className="sidebar">
        <Sidebar
          visible={visibleRight}
          position="right"
          onHide={() => setVisibleRight(false)}
        >
          <div className="sidebar-logo">
            <img src={logo} />
          </div>

          <div className="user-infos">
            <h2>Welcome {username}</h2>
            <p>
              Predicode, the website that take your app source code and predict
              your app rating to have an idea on how to proceed with your idea
            </p>
          </div>
          <div className="sidebar-buttons">
            {isAdmin && (
              <div className="logout">
                <Button
                  label="Admin Panel"
                  className="btn logout"
                  onClick={goAdminPage}
                />
              </div>
            )}
            <div className="logout sidebar-logout">
              <Button
                label="Logout"
                className="btn logout"
                onClick={handleLogout}
              />
            </div>
          </div>
        </Sidebar>
      </section>
    </div>
  );
};

export default Navbar;
