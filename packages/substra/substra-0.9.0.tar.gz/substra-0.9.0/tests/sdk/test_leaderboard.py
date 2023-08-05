# Copyright 2018 Owkin, inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import substra

from .. import datastore
from .utils import mock_requests


def test_leaderboard(client, mocker):
    item = datastore.LEADERBOARD

    m = mock_requests(mocker, "get", response=item)

    response = client.leaderboard("magic-key")

    assert response == item
    m.assert_called()


def test_leaderboard_not_found(client, mocker):
    mock_requests(mocker, "get", status=404)

    with pytest.raises(substra.sdk.exceptions.NotFound):
        client.leaderboard("magic-key")
