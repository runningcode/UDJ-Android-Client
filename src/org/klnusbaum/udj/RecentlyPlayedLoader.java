/**
 * Copyright 2011 Kurtis L. Nusbaum
 *
 * This file is part of UDJ.
 *
 * UDJ is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * UDJ is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with UDJ.  If not, see <http://www.gnu.org/licenses/>.
 */
package org.klnusbaum.udj;


import android.content.Context;
import android.accounts.Account;

import java.util.List;
import java.io.IOException;

import org.json.JSONException;

import org.apache.http.auth.AuthenticationException;
import org.apache.http.ParseException;

import org.klnusbaum.udj.network.ServerConnection;
import org.klnusbaum.udj.containers.LibraryEntry;
import org.klnusbaum.udj.exceptions.PlayerAuthException;
import org.klnusbaum.udj.exceptions.PlayerInactiveException;

public class RecentlyPlayedLoader extends MusicSearchLoader{

  public RecentlyPlayedLoader(Context context, Account account){
    super(context, account);
  }

  @Override
  protected MusicSearchResult doSearch(long playerId, String authToken) throws
    JSONException, ParseException, IOException,
    AuthenticationException, PlayerInactiveException, PlayerAuthException
  {
    List<LibraryEntry> list =
        ServerConnection.getRecentlyPlayedLibEntries(40, playerId, authToken);
    return new MusicSearchResult(list);
  }
}
