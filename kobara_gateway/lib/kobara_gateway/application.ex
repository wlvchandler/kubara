defmodule KobaraGateway.Application do
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      KobaraGateway.MatchingEngine
    ]

    opts = [strategy: :one_for_one, name: KobaraGateway.Supervisor]
    Supervisor.start_link(children, opts)
  end
end