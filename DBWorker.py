'''from pg_database import Artist
from pg_database import User
from pg_database import Subscribe
from pg_database import conn


def logUser(uTgID, uUsername, uName, uLname):
    newUser = User(id=uTgID, username=uUsername, name=uName, lastName=uLname)
    rows = newUser.save()
    if rows == 0:
        return newUser.save(force_insert=True)
    else:
        return rows


def logArtist(aLogin, aLastWork, aLastThumb, aLastPost):
    newArtist = Artist.get_or_none(Artist.login == aLogin)
    print("1. newArtist:", newArtist)
    if newArtist:
        newArtist.upd(work=aLastWork, thumb=aLastThumb, post=aLastPost)
        print("2.NotNewArtist:", newArtist)
    else:
        newArtist = Artist(login=aLogin, lastWork=aLastWork, lastThumb=aLastThumb, lastPost=aLastPost)
    rows = newArtist.save()
    return rows

'''
'''
def addSubs(user, artist):
    artistID = Artist.select(Artist.login == artist).dicts
     # HERE should be get ID by name
    subscribe = Subscribe(userID=user, artistID=artistID)
    subscribe.save()


def ifSubscribe(user, artist):
    try:
        sub = Subscribe.select(Subscribe.userID == user, Artist.login == artist).join(Subscribe)[0]
        print('subs type', type(sub))
        print(sub)
    except Exception as e:
        return None
'''
'''
def test():
    sub = User.select()
    xyu = list(sub)
    print(type(xyu))
    print(xyu)
'''
